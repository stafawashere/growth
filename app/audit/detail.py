"""The mechanical bound on an audit_log detail, per docs/plan/13-ai-engineering.md item 9
under "Where app/providers/guard.py is wrong" (about line 365).

That item names two checks for the detail field: "a rejection of any value matching a key
shape, and no free-form string from a provider response", plus "a maximum length". Every
09-security-and-privacy.md writer was well behaved by inspection, and inspection is exactly
the control that stops holding at the next call site (13-ai-engineering.md:365), so this
module is the one place every writer calls before a detail reaches json.dumps.

What is implemented here, and what is not.

JSON-plain. A detail may only be None, a str, an int, a float, a bool, a list of such
values, or a dict with str keys holding such values, recursively. Anything else, an object,
a set, bytes, a provider SDK response object, cannot reach the column at all.

Key shape, by field name. docs/plan/07-ai-provider-layer.md's "Rules that hold without
exception" (07:341) and 09-security-and-privacy.md:64 both say no key or any part of one,
including a masked prefix, ever reaches an audit_log detail. A dict key is refused when its
letters and digits, case-folded, name a secret the way the code or the plan names one:
"apikey" (every *_API_KEY variable, the "x-api-key" header app/providers/anthropic.py sends,
the api_key local that carries it), a name that is or ends in "key" (07:337 and 09:60 call
the stored secret a "key"), a name that is or ends in "token" but not "tokens" (the session
token app/auth/service.py returns under "token", the bearer token of 07:357 and 09:70, the
OAuth token of 07:357; "tokens" is left alone because budget details carry cap_tokens),
"secret" (07:347, 09:70), "passphrase" (07:337, 09:194), "bearer" (07:232, 07:357) and
"oauth" (07:357, 07:365).

Key shape, by value. Neither document states a value pattern a provider key follows, so this
cannot match on a vendor prefix recalled from memory. Two things are mechanically knowable
and both are checked, on every string value and every dict key, recursively:

1. The live value of each provider key environment variable the code or the plan names,
   read from os.environ at call time so a key configured after import still binds.
   PROVIDER_KEY_ENV_VARS is the list; tests/audit/test_detail_bound.py scans app/, 07 and 09
   for *_API_KEY names and fails if any is missing from it. ANTHROPIC_API_KEY is read by
   app/main.py and app/providers/anthropic.py AnthropicProvider; CLAUDEBOX_API_KEY is named at 07:232
   and 09:70; OLLAMA_API_KEY at 07:213. An unset or empty variable is skipped, since an empty
   string is contained in every string.
2. The text of a credential form the code sends or the plan names, case-folded. "x-api-key"
   is the header app/providers/anthropic.py _headers builds with the key as its value (the
   test reads every _headers dict in app/providers and fails if a runtime-valued header is
   missing from CREDENTIAL_VALUE_FORMS). "bearer" is the form of the claudebox credential,
   07:232 and 07:357.

Residual gaps, reported rather than papered over. A key that is not configured in this
process's environment, for instance one decrypted from provider_configs for a single request
(07:341, 09:62), and that sits under a field name outside the list above and carries no
credential-form text, cannot be recognised: the plan gives no key prefix to recognise it by
shape. "authorization" is not in either list because no adapter sends that header and neither
document names it; a bearer credential still trips the "bearer" value form. OpenRouter and
Google are named as providers throughout 07 and 09 but neither document nor app/providers
gives their key material an env var name, a header name or a value prefix. And a provider
key env var set to a very short value makes every audit write whose detail contains that text
refuse, which fails closed; the plan gives no minimum key length to exempt it by.

Length bound not implemented, and left as an open operator decision. 13-ai-engineering.md:365
asks for "a maximum length" and gives no number. Neither 09-security-and-privacy.md nor
06-architecture.md's audit_log table gives one either, and no other number in any of them is
a value a detail-length bound could be derived from by arithmetic. Per the standing rule
against filling a threshold with a plausible-looking value, no length bound is enforced here
until the operator sets one.
"""
import os
import re

PROVIDER_KEY_ENV_VARS = ("ANTHROPIC_API_KEY", "CLAUDEBOX_API_KEY", "OLLAMA_API_KEY")

CREDENTIAL_VALUE_FORMS = ("x-api-key", "bearer")

_SECRET_NAME_FRAGMENTS = ("apikey", "secret", "passphrase", "bearer", "oauth")
_SECRET_NAME_SUFFIXES = ("key", "token")

_NON_ALPHANUMERIC = re.compile(r"[^a-z0-9]")


def _names_a_secret(field_name):
   normalized = _NON_ALPHANUMERIC.sub("", field_name.lower())
   contains_fragment = any(fragment in normalized for fragment in _SECRET_NAME_FRAGMENTS)
   ends_with_suffix = any(normalized.endswith(suffix) for suffix in _SECRET_NAME_SUFFIXES)

   return contains_fragment or ends_with_suffix


def _configured_provider_keys():
   configured = []

   for env_var in PROVIDER_KEY_ENV_VARS:
      value = os.environ.get(env_var)
      is_configured = value is not None and value != ""

      if is_configured:
         configured.append(value)

   return configured


def _carries_key_material(text, configured_keys):
   folded = text.lower()
   has_credential_form = any(form in folded for form in CREDENTIAL_VALUE_FORMS)
   has_configured_key = any(key in text for key in configured_keys)

   return has_credential_form or has_configured_key


def bind_audit_detail(detail, path="detail"):
   """Return detail unchanged if it is JSON-plain and carries nothing key-shaped, else raise
   ValueError naming the offending path. Neither the value nor the dict key that tripped the
   check is included in the message, so raising cannot itself leak the thing it refuses."""
   return _bind(detail, path, _configured_provider_keys())


def _bind(detail, path, configured_keys):
   if detail is None or isinstance(detail, (bool, int, float)):
      return detail

   if isinstance(detail, str):
      if _carries_key_material(detail, configured_keys):
         raise ValueError(f"{path} carries provider key material")

      return detail

   if isinstance(detail, list):
      return [_bind(item, f"{path}[{index}]", configured_keys) for index, item in enumerate(detail)]

   if isinstance(detail, dict):
      bound = {}

      for index, (key, value) in enumerate(detail.items()):
         if not isinstance(key, str):
            raise ValueError(f"{path} has a non-string key")

         if _carries_key_material(key, configured_keys):
            raise ValueError(f"{path} key {index} carries provider key material")

         child_path = f"{path}.{key}"

         if _names_a_secret(key):
            raise ValueError(f"{child_path} is named for a secret")

         bound[key] = _bind(value, child_path, configured_keys)

      return bound

   raise ValueError(f"{path} is not JSON-plain: {type(detail).__name__}")
