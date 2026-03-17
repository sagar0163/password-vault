# Architecture Document: Secure Password Vault

## 1. System Overview

Secure Password Vault is a Python-based terminal application that manages passwords locally. It uses a simple encryption mechanism to protect stored credentials and provides a menu-driven interface for user interaction.

## 2. Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interface Layer                     │
│              (Terminal Menu System)                        │
│              - Navigation (up/down/enter)                  │
│              - Display (password list, strength meter)    │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                   Business Logic Layer                      │
│  ┌─────────────────┐  ┌─────────────────┐                │
│  │ Password        │  │ Vault           │                │
│  │ Generator       │  │ Manager         │                │
│  │ - Random chars  │  │ - Add/Edit/Del  │                │
│  │ - Length config │  │ - Search        │                │
│  │ - Strength calc │  │ - Load/Save     │                │
│  └─────────────────┘  └─────────────────┘                │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                    Security Layer                           │
│  ┌─────────────────┐  ┌─────────────────┐                │
│  │ Encryption      │  │ Master Password │                │
│  │ (XOR)          │  │ Handler         │                │
│  └─────────────────┘  └─────────────────┘                │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                     Data Layer                              │
│              (Local File: ~/.password_vault)               │
└─────────────────────────────────────────────────────────────┘
```

## 3. Core Components

### Password Generator
- Generates random passwords using configurable character sets
- Calculates password strength (0-100 score)
- Provides strength rating (Weak/Medium/Strong)

### Vault Manager
- CRUD operations for password entries
- Search functionality
- Auto-lock timer management

### Encryption Module
- XOR-based encryption (for demonstration)
- Master password verification
- Secure memory handling

### Clipboard Handler
- Uses pyperclip for cross-platform clipboard access
- Auto-clear clipboard after timeout (optional)

## 4. Data Model

### Password Entry
```python
{
    "id": "unique-id",
    "service": "website or service name",
    "username": "user@email.com",
    "password": "encrypted-password",
    "strength": 85,
    "created_at": "timestamp"
}
```

### Storage Format
JSON file stored at `~/.password_vault`, encrypted with master password.

## 5. File Structure

```
password-vault/
├── vault.py           # Main application
├── specs/            # Documentation
└── README.md
```

---

*Document Version: 1.0*  
*Created: 2026-03-17*
