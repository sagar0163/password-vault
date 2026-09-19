# Secure Password Vault 🔐

A terminal-based password manager with encryption.

## Features

- 🔑 **Password Generator** - Generate strong passwords
- 🔒 **Encrypted Storage** - AES-256-GCM encryption with PBKDF2 key derivation
- 🔍 **Search** - Quick search through passwords
- 📋 **Clipboard** - Copy passwords easily
- 💪 **Strength Checker** - Evaluate password strength
- ⏰ **Auto-Lock** - Lock after 5 minutes of inactivity

## Installation

```bash
pip install pyperclip cryptography
python3 vault.py
```

## Usage

### Menu Options
- 🔍 Search passwords
- ➕ Add new password
- 📋 Generate password
- ⚙️ Settings
- 🚪 Exit

### Controls
- ↑↓ Navigate
- Enter Select
- d Delete
- q Back

## Password Strength

| Score | Rating |
|-------|--------|
| 0-49 | 🔴 Weak |
| 50-74 | 🟡 Medium |
| 75-100 | 🟢 Strong |

## Data Storage

Passwords stored encrypted in: `~/.password_vault`

## Security Note

The vault is encrypted with AES-256-GCM (authenticated encryption). The
master password is stretched into a 256-bit key via PBKDF2-HMAC-SHA256 with
600,000 iterations and a per-vault random salt, so the ciphertext is
non-malleable and tampering is detected. For production, also consider:
- Use `keyring` for secure key storage
- Add two-factor authentication

## License

MIT License
# Updated
# Update
