# Business Requirements Document (BRD)

## Project Overview
- **Project Name**: Password Vault
- **Type**: Terminal-based Password Manager
- **Core Functionality**: A secure terminal application for storing, generating, and managing passwords with encryption
- **Target Users**: Individuals who need a simple, CLI-based password management solution

## Features
1. **Password Generator** - Generate strong, random passwords
2. **Encrypted Storage** - XOR encryption with master password protection
3. **Quick Search** - Fast search through stored passwords
4. **Clipboard Integration** - One-click copy to clipboard
5. **Password Strength Checker** - Evaluate password strength (0-100 score)
6. **Auto-Lock** - Automatic lock after 5 minutes of inactivity

## Tech Stack
- **Language**: Python 3
- **Dependencies**: pyperclip (clipboard), cryptography (optional for production)
- **Storage**: Local file (~/.password_vault)
- **Encryption**: XOR (demonstration) / AES (production recommendation)

## User Stories
1. As a user, I want to generate strong passwords so that my accounts are secure
2. As a user, I want to store passwords encrypted so that only I can access them
3. As a user, I want to quickly search for passwords so that I can find login credentials fast
4. As a user, I want passwords copied to clipboard so that I can paste them easily
5. As a user, I want auto-lock for security when I'm away

## Requirements
- Python 3.x
- pyperclip package
- Terminal emulator
- Master password for encryption/decryption

## Future Enhancements
- AES-256 encryption instead of XOR
- Import/Export functionality
- Password categories/folders
- Browser integration
- Two-factor authentication support
- Cloud sync capability
