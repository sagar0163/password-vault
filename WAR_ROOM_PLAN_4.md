# WAR_ROOM_PLAN_4.md

## Tasks
- [x] Fix master password echo: `draw_login` uses `curses.noecho()` instead of `curses.nocho()` (or correctly toggles echo).
- [x] Fix Add-entry password echo: `get_input` must not echo when asking for a password field.
- [ ] Implement clipboard auto-clear: Create a background thread or process that clears the clipboard after ~45s.
- [ ] Implement `[c]` in generator view: copy generated password to clipboard with auto-clear.
- [ ] Implement `[s]` Save in generator view: save the generated password as a new entry.
- [ ] Implement `[c]` and `[u]` in entry view: copy password and username to clipboard with auto-clear.
