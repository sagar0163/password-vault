# War Room Plan — Issue #2: Replace XOR with PBKDF2 + AES-256-GCM

- [x] Add `cryptography` to requirements.txt and remove XOR functions from vault.py
- [x] Implement `vault_encrypt`/`vault_decrypt` (PBKDF2-HMAC-SHA256 600k + AES-256-GCM, `magic||version||salt||nonce||ct` header)
- [x] Define `VaultError` and surface GCM auth failure as an explicit error (no silent empty vault)
- [x] Wire `PasswordVault.load/save` to new binary format
- [x] Update tests: round-trip, wrong password, tamper-detection; drop `simple_encrypt/simple_decrypt` test
- [x] Update README/ARCHITECTURE/BRD docs that reference XOR
- [ ] Run pytest, fix failures, final cleanup + commit + push