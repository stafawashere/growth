"""The fallback chain and cooldowns for every role (docs/plan/11-phased-delivery.md P6 scope item 5,
cut to one student on the operator's delegation of 2026-09-24).

A role runs down an ordered chain of links. The operator's Claude subscription comes first; the
paid API follows only when GROWTH_AI_BACKEND=api allows it (app/main.py provider_links); when no
link may run, the caller degrades to static feedback exactly as it did before there was a chain:
the tutor shows the deterministic payload, a grading point stays provisional, and a call stopped by
a usage limit is queued for the drain.

Each link is wrapped in its own GuardedProvider, because the two backends are capped in different
units: the subscription by call counts (SubscriptionPacingCaps), the API by the per-role dollar and
token caps and the persistent developer spend cap. A budget or pacing stop refuses before its
link's call, so a fallback can never spend past a cap on the link it falls to; the stop moves the
call to the next link and puts nothing on cooldown, since the guard's own refusal costs no call.

A link goes on cooldown after a provider-side failure, per role, in this process:

- a usage limit (SubscriptionLimitReached) cools the link for LIMIT_COOLDOWN, the drain's own
  retry interval, so a student who reopens feedback while the window holds starts no CLI process;
- FAILURES_BEFORE_COOLDOWN consecutive failures of any other kind cool it for FAILURE_COOLDOWN.

A call that finds a link cooling skips it without starting anything. When no link answered, the
first link's stop or failure is raised, a skipped link's as CoolingDown, which names the failure
that started the cooldown so a limit still reads as a limit to the caller that queues it. A link
that could not run at all (RefusedBeforeWire: no CLI installed, no key) is reported only when no
other link got as far as a stop or a failure, because it says nothing about the call.
"""
import threading
from dataclasses import dataclass, field
from datetime import timedelta

from app.auth.service import utc_now
from app.providers.anthropic import AnthropicProvider
from app.providers.base import Provider, RefusedBeforeWire
from app.providers.guard import (
   BudgetStopped,
   DevSpendCapExceeded,
   GuardedProvider,
   ProviderCallFailed,
   SubscriptionPacingCaps,
)
from app.providers.subscription import SubscriptionLimitReached, SubscriptionProvider

SUBSCRIPTION_LINK = "subscription"
API_LINK = "api"
REPLAY_LINK = "replay"

LIMIT_COOLDOWN = timedelta(minutes=30)
FAILURE_COOLDOWN = timedelta(seconds=60)
FAILURES_BEFORE_COOLDOWN = 3

LIMIT_FAILURE = SubscriptionLimitReached.__name__


@dataclass(frozen=True)
class ChainLink:
   """One backend a role may run on. pacing is the SubscriptionPacingCaps a subscription link is
   paced by, None for a link capped in dollars; pays marks the one link that spends real money, so
   only it is tracked against the developer spend cap."""

   name: str
   provider: Provider
   pacing: object = None
   pays: bool = False


class CoolingDown(ProviderCallFailed):
   """A link skipped because it is cooling. exception_type is the failure that started the
   cooldown, so a caller that recognises a usage limit by name still sees one."""


@dataclass
class LinkState:
   consecutive_failures: int = 0
   cooling_until: object = None
   cooling_because: str | None = None


@dataclass
class CooldownBoard:
   """Cooldowns per role and link, for the life of the process. One board lives on Settings, so a
   test's application never sees another's cooldowns."""

   states: dict = field(default_factory=dict)
   lock: threading.Lock = field(default_factory=threading.Lock)

   def _state(self, role, link_name):
      key = (role, link_name)

      if key not in self.states:
         self.states[key] = LinkState()

      return self.states[key]

   def cooling(self, role, link_name, now):
      """The failure type that cooled the link, or None when it may run."""
      with self.lock:
         state = self._state(role, link_name)
         has_cooldown = state.cooling_until is not None
         still_cooling = has_cooldown and now < state.cooling_until

         if not still_cooling:
            return None

         return state.cooling_because

   def succeeded(self, role, link_name):
      with self.lock:
         state = self._state(role, link_name)
         state.consecutive_failures = 0
         state.cooling_until = None
         state.cooling_because = None

   def failed(self, role, link_name, failure_type, now):
      with self.lock:
         state = self._state(role, link_name)
         state.consecutive_failures = state.consecutive_failures + 1
         is_limit = failure_type == LIMIT_FAILURE
         is_repeated_failure = state.consecutive_failures >= FAILURES_BEFORE_COOLDOWN

         if is_limit:
            state.cooling_until = now + LIMIT_COOLDOWN
            state.cooling_because = failure_type
         elif is_repeated_failure:
            state.cooling_until = now + FAILURE_COOLDOWN
            state.cooling_because = failure_type

   def snapshot(self, now):
      """Every link that is cooling now, for GET /settings/providers."""
      with self.lock:
         cooling = []

         for (role, link_name), state in sorted(self.states.items()):
            has_cooldown = state.cooling_until is not None
            still_cooling = has_cooldown and now < state.cooling_until

            if still_cooling:
               cooling.append({
                  "role": role,
                  "link": link_name,
                  "until": state.cooling_until.isoformat(),
                  "because": state.cooling_because,
               })

         return cooling


def failure_type_of(raised):
   is_bounded = isinstance(raised, ProviderCallFailed)

   if is_bounded:
      return raised.exception_type

   return type(raised).__name__


class FallbackChain(Provider):
   """The provider a role's caller wires. last_accounting is the accounting of the link call that
   answered, or of the last link call that reached a provider, so the tutor's per-item ceilings
   count this call once whichever link served it."""

   def __init__(self, links, db, user_id, caps=None, clock=None, board=None, guard_options=None):
      self._links = tuple(links)
      self._db = db
      self._user_id = user_id
      self._caps = caps or {}
      self._clock = clock or utc_now
      self._board = board if board is not None else CooldownBoard()
      self._guard_options = guard_options or {}
      self.last_accounting = None
      self.served_by = None

   def guarded(self, link):
      return GuardedProvider(
         link.provider,
         self._db,
         self._user_id,
         clock=self._clock,
         caps=self._caps,
         dev_spend_track=link.pays,
         subscription_pacing=link.pacing,
         **self._guard_options,
      )

   def generate(self, request):
      return self._run(request, lambda guarded: guarded.generate(request))

   def stream(self, request):
      """The chain decides a link before any text is shown, so a stream is the chosen link's whole
      result as one delta, the shape SubscriptionProvider.stream already gives."""
      result = self.generate(request)

      if result.text:
         yield {"type": "text", "delta": result.text}

      return result

   def _run(self, request, call):
      self.last_accounting = None
      self.served_by = None
      first_failure = None
      first_unavailable = None

      for link in self._links:
         now = self._clock()
         cooled_by = self._board.cooling(request.role, link.name, now)
         is_cooling = cooled_by is not None

         if is_cooling:
            skipped = CoolingDown(link.name, request.model, request.role, cooled_by)
            first_failure = first_failure or skipped

            continue

         guarded = self.guarded(link)

         try:
            result = call(guarded)
         except RefusedBeforeWire as unavailable:
            first_unavailable = first_unavailable or unavailable

            continue
         except (BudgetStopped, DevSpendCapExceeded) as stopped:
            first_failure = first_failure or stopped

            continue
         except ProviderCallFailed as failed:
            self._keep_accounting(guarded)
            self._board.failed(request.role, link.name, failure_type_of(failed), self._clock())
            first_failure = first_failure or failed

            continue

         self._keep_accounting(guarded)
         self._board.succeeded(request.role, link.name)
         self.served_by = link.name

         return result

      if first_failure is not None:
         raise first_failure

      if first_unavailable is not None:
         raise first_unavailable

      raise BudgetStopped(request.role, ("no_provider_link",))

   def _keep_accounting(self, guarded):
      has_accounting = guarded.last_accounting is not None

      if has_accounting:
         self.last_accounting = guarded.last_accounting


def links_from_settings(settings, links_field, provider_field):
   """The configured chain, or, where only a provider was set (every test that wires a double), a
   one-link chain over it with the pacing and tracking the old single-provider wiring used."""
   links = getattr(settings, links_field, None)

   if links:
      return tuple(links)

   provider = getattr(settings, provider_field, None)

   if provider is None:
      return ()

   return (single_link(provider, settings.subscription_pacing),)


def single_link(provider, configured_pacing):
   is_live_api = isinstance(provider, AnthropicProvider)
   is_on_the_subscription = isinstance(provider, SubscriptionProvider)

   if is_on_the_subscription:
      return ChainLink(SUBSCRIPTION_LINK, provider, pacing=configured_pacing or SubscriptionPacingCaps())

   if is_live_api:
      return ChainLink(API_LINK, provider, pays=True)

   return ChainLink(getattr(provider, "name", type(provider).__name__), provider)


def chain_for(settings, db, user_id, links_field, provider_field, caps, clock=None):
   """The provider a role's caller wires, or None when no link is configured, which is the
   no-provider degradation every caller already handles."""
   links = links_from_settings(settings, links_field, provider_field)

   if not links:
      return None

   return FallbackChain(links, db, user_id, caps=caps, clock=clock, board=settings.provider_cooldowns)
