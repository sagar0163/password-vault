# Plan for Issue #3

- [ ] Fix `PasswordVault.save()` to write to a temporary file first, then `os.replace()` it over the original file, to make the save atomic.
- [ ] In `PasswordVault.save()`, ensure the temp file (and thus the final file) is created with `0600` permissions.
- [ ] Update `PasswordManagerCLI.draw_login()` to catch `VaultError` when initializing `PasswordVault`, and display an error instead of crashing/clearing.
- [ ] Add tests to verify that `save()` is atomic, that file permissions are set correctly (0600), and that wrong password handling works properly.
