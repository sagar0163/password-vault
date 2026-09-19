# Architecture Document

## System Architecture

```
┌─────────────────────────────────────────────┐
│            Password Vault App                │
├─────────────────────────────────────────────┤
│  ┌─────────────┐  ┌──────────────────────┐  │
│  │   UI Layer  │  │   Business Logic     │  │
│  │  (CLI Menu) │◄─┤   - Password Gen     │  │
│  └─────────────┘  │   - Crypto Module    │  │
│                   │   - Storage Manager  │  │
│                   └──────────────────────┘  │
│                           │                  │
│                   ┌───────▼────────┐         │
│                   │  Data Layer    │         │
│                   │ ~/.password_vlt│         │
│                   └────────────────┘         │
└─────────────────────────────────────────────┘
```

## Components

### 1. UI Layer (vault.py)
- Command-line menu interface
- User input handling
- Display formatting

### 2. Business Logic
- **PasswordGenerator**: Creates random secure passwords
- **CryptoEngine**: Handles AES-256-GCM encryption/decryption (PBKDF2-HMAC-SHA256 key derivation)
- **VaultManager**: CRUD operations on password entries
- **StrengthChecker**: Analyzes password complexity

### 3. Data Layer
- JSON-based storage format
- Encrypted file at ~/.password_vault

## Data Flow

1. **Add Password**: User Input → Encrypt → Write to Vault File
2. **Get Password**: Read Vault → Decrypt → Display/Search → Copy to Clipboard
3. **Generate Password**: Random chars → Strength Check → Return

## Security Considerations

- Master password stretched via PBKDF2-HMAC-SHA256 (600,000 iterations, random salt)
- AES-256-GCM authenticated encryption (tamper detection)
- Auto-lock timer (5 minutes)
- Clipboard auto-clear recommended

## File Structure

```
password-vault/
├── vault.py           # Main application
├── requirements.txt   # Dependencies
├── README.md         # Documentation
├── SECURITY.md       # Security policy
├── CONTRIBUTING.md   # Contribution guidelines
└── specs/
    ├── BRD.md        # This file
    └── ARCHITECTURE.md
```
