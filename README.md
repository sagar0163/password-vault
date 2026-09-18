# Secure Password Vault 🔐

A terminal-based password manager with encryption.

## Features

- 🔑 **Password Generator** - Generate strong passwords
- 🔒 **Encrypted Storage** - XOR encryption with master password
- 🔍 **Search** - Quick search through passwords
- 📋 **Clipboard** - Copy passwords easily
- 💪 **Strength Checker** - Evaluate password strength
- ⏰ **Auto-Lock** - Lock after 5 minutes of inactivity

## Installation

```bash
pip install pyperclip
python3 vault.py
```

## Usage

### Menu Options
- 🔍 Search passwords (type to dynamically filter)
- ➕ Add new password
- 📋 Generate password
- 📤 Export to CSV
- 📥 Import from CSV
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
Automatic timestamped backups are created alongside the vault file before every save.

## Security Note

This uses simple XOR encryption for demonstration. For production, consider:
- Use `keyring` for secure key storage
- Use `cryptography` library for AES
- Add two-factor authentication

## License

MIT License
# Updated
# Update
