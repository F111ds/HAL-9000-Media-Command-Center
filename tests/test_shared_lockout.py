"""The right code at the phone server also lifts HAL's lockout for that phone (and the other way round)."""
import sys as _sys
from pathlib import Path as _Path
ROOT = _Path(__file__).resolve().parents[1]  # the project folder
_sys.path.insert(0, str(ROOT))
import types
import mobile_server as m
import hal_server as hs

assert m._hal_mod is hs
ip = "100.111.60.101"
m._token_bytes = b"right-code"
for _ in range(hs.AUTH_MAX_FAILURES):
    hs.AUTH_FAILURES.record(ip)
assert hs.AUTH_FAILURES.blocked_for(ip)          # HAL locked the phone out after wrong tries

sent = []
h = types.SimpleNamespace(client_address=(ip, 5000), headers={"X-Mobile-Token": "right-code"},
                          send_json=lambda *a, **k: sent.append(a))
h.ip = ip
h.authorized = lambda: m.MobileHandler.authorized(h)
assert m.MobileHandler._auth_ok(h) is True and not sent
assert not hs.AUTH_FAILURES.blocked_for(ip)      # the right code at the phone server cleared it

# the other way: HAL accepting the code clears the phone server's count
for _ in range(m.AUTH_MAX_FAILURES):
    m.AUTH_FAILURES.record(ip)
hs.AUTH_OK_HOOKS[:] = [m.AUTH_FAILURES.clear]
for hook in hs.AUTH_OK_HOOKS:
    hook(ip)
assert not m.AUTH_FAILURES.blocked_for(ip)
print("shared lockout OK")
