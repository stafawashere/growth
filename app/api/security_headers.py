"""CSP and CORS for every response, docs/plan/09-security-and-privacy.md's "Transport and
hosting" section (CORS and CSP paragraphs, around lines 158 to 160).

09's CORS paragraph gives no allowlist to widen and no configuration knob to add one: the API
and the client are same-origin, served by the same process, and there is no reason for a
third-party origin to call this API. That is satisfied by omission, not by code here: no
CORSMiddleware is installed anywhere in this application, so no request, cross-origin or same-
origin, preflight or not, ever gets an Access-Control-Allow-Origin header back. This module does
not add one either.

09's CSP paragraph fixes default-src 'self', no unsafe-inline or unsafe-eval for scripts, styles
restricted to self, img-src 'self' blob: for camera capture, connect-src 'self', frame-ancestors
'none', object-src 'none' and base-uri 'none', plus style-src-attr 'unsafe-inline' because MathLive
positions every formula box through run-time style attributes that no build hash can cover. The
built index.html carries no inline style or script element, so style-src 'self' needs no hashes.

09 sets no HSTS max-age and no per-IP rate-limit number, so neither is built here.
"""
from starlette.middleware.base import BaseHTTPMiddleware

CONTENT_SECURITY_POLICY = (
   "default-src 'self'; "
   "script-src 'self'; "
   "style-src 'self'; "
   "style-src-attr 'unsafe-inline'; "
   "img-src 'self' blob:; "
   "connect-src 'self'; "
   "frame-ancestors 'none'; "
   "object-src 'none'; "
   "base-uri 'none'"
)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
   """Stamps the CSP header onto every response, error responses included, since
   BaseHTTPMiddleware wraps the whole ASGI call including a 404 or a 405."""

   async def dispatch(self, request, call_next):
      response = await call_next(request)
      response.headers["Content-Security-Policy"] = CONTENT_SECURITY_POLICY

      return response
