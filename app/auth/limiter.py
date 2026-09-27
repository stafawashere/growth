"""The per-IP tier on the three unauthenticated credential routes: POST /auth/signup, /auth/login and
/auth/recovery/reset (ruled 2026-09-27, narrowing docs/plan/09-security-and-privacy.md's
unauthenticated-route limit to these three).

A sliding window of request times per peer address, held for the process lifetime. It is keyed on
request.client.host. On the default loopback bind every local caller is 127.0.0.1, so the limit
works as one bucket there. Behind a reverse proxy on the same machine, uvicorn's proxy headers
(on by default, trusting 127.0.0.1) replace the peer with the X-Forwarded-For address, so each
remote client gets its own window.
The route calls it after the body has parsed, so a cross-site text/plain loop that only earns
422s never spends the bucket, and before any scrypt work or database write.
"""
import math
import threading
from collections import OrderedDict, deque

DEFAULT_LIMIT_COUNT = 10
DEFAULT_LIMIT_WINDOW_SECONDS = 60
MAX_TRACKED_KEYS = 1024


def oldest_has_expired(moments, cutoff):
   has_moments = len(moments) > 0

   return has_moments and moments[0] <= cutoff


class SlidingWindowLimiter:
   def __init__(self, max_keys=MAX_TRACKED_KEYS):
      self.max_keys = max_keys
      self.windows = OrderedDict()
      self.lock = threading.Lock()

   def prune(self, now, window_seconds):
      cutoff = now - window_seconds

      for key in list(self.windows):
         moments = self.windows[key]

         while oldest_has_expired(moments, cutoff):
            moments.popleft()

         is_empty = len(moments) == 0

         if is_empty:
            del self.windows[key]

      while len(self.windows) > self.max_keys:
         self.windows.popitem(last=False)

   def admit(self, key, now, count, window_seconds):
      """Records the request and returns None when it is within the limit, or the whole seconds
      until the oldest request in the window expires when it is not. A refused request is not
      recorded, so a caller that keeps retrying is let back in once the window moves on."""
      with self.lock:
         self.prune(now, window_seconds)
         moments = self.windows.get(key)

         if moments is None:
            moments = deque()
            self.windows[key] = moments

         self.windows.move_to_end(key)
         is_over = len(moments) >= count

         if is_over:
            wait = moments[0] + window_seconds - now

            return max(1, math.ceil(wait))

         moments.append(now)

         while len(self.windows) > self.max_keys:
            self.windows.popitem(last=False)

         return None

   def tracked_keys(self):
      with self.lock:
         return tuple(self.windows)
