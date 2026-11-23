# HAL 9000 Media Command Center: notes for Claude

Windows-only Python app: a phone/TV/desktop command center for a home media PC. Plain standard library
(`http.server`), no web framework, no build step. The only extra package is `psutil`.

## Layout
- `mobile_server.py`: the hub (port 8765). Serves the phone app (`app_page.py`, `mobile_page.py`) and starts
  HAL inside itself (port 8766) unless `--no-hal`.
- `hal_server.py`: HAL 9000 (monitoring, alerts, Siri, the phone "HAL" page). `hal_tv_page.py`: his TV screen.
- `nzb_command_center.py`, `system_command_center.py`: desktop apps (tkinter).
- `tv-launcher/`: the Android TV home screen (Gradle project) and its install scripts.
- Pages are HTML/CSS/JS kept as big Python strings. A stray quote breaks the whole page, so after
  editing page JS, extract the `<script>` and run `node --check` on it (the tests do this too).

## Running and testing
- Tests: `python tests/run_all.py` (each test is a plain script; `python tests/test_x.py` runs one).
  `test_tv_control.py` can be flaky in the full suite; run it alone before calling it broken.
- Look around without real services: `python hal_server.py --demo --host 127.0.0.1 --port 9766`, then
  `http://127.0.0.1:9766/pair` (on the same PC) shows the access code. The page reads it from
  `localStorage.hal_token`; the TV screen takes it as `/tv#k=<code>`.
- `.claude/launch.json` has `hal-demo` (9766) and `phone-server` (9765/9767) for the browser preview.
  **Never use 8765/8766 for testing**: the owner's live server runs there.
- Phone screens: check at 390x844. TV: 1920x1080.

## Rules
- **Line endings are LF** (`core.autocrlf=false`). On Windows, Python's `write_text` turns files CRLF and
  rewrites every line. Use `write_bytes` or `open(..., "w", newline="\n")`, and check `git diff --stat`
  before committing: a small change must not show thousands of lines.
- **Never commit secrets or per-machine state.** `.gitignore` lists them (config/keys, `*_settings.json`,
  `*.keystore`, `github_token.txt`, logs, `tv_*` state). Screenshots for the README use demo data only.
- Commits use the GitHub noreply address, never a personal email.
- Keep the README's order: phone app, then the NZB Command Center, TV home screen, HAL on the TV, Siri.
- Desktop app with WebGL (`hal_desktop.py`, where present): keep PySide6 at 6.11.3; 6.12.0 crashes in
  Qt WebEngine.
