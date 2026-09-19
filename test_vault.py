"""Unit tests for Password Vault"""

import pytest
from unittest.mock import Mock, patch
from pathlib import Path
from vault import (
    PasswordVault,
    PasswordGenerator,
    VaultError,
    vault_encrypt,
    vault_decrypt,
)


@pytest.fixture(autouse=True)
def mock_pyperclip():
    """Mock pyperclip for all tests to avoid touching real clipboard."""
    with patch('vault.pyperclip') as mock:
        yield mock


class TestPasswordGenerator:
    def test_generate_password_length(self):
        password = PasswordGenerator.generate(length=20)
        assert len(password) == 20
    
    def test_generate_password_with_special_chars(self):
        password = PasswordGenerator.generate(length=16, lowercase=False, uppercase=False, digits=False, symbols=True)
        assert any(c in password for c in '!@#$%^&*()_+-=[]{}|;:,.<>?')
    
    def test_generate_password_numbers(self):
        password = PasswordGenerator.generate(length=16, lowercase=False, uppercase=False, symbols=False, digits=True)
        assert any(c.isdigit() for c in password)
    
    def test_generate_password_uppercase(self):
        password = PasswordGenerator.generate(length=16, lowercase=False, digits=False, symbols=False, uppercase=True)
        assert any(c.isupper() for c in password)

    def test_generate_password_lowercase(self):
        password = PasswordGenerator.generate(length=16, uppercase=False, digits=False, symbols=False, lowercase=True)
        assert any(c.islower() for c in password)


class TestPasswordVault:
    def test_vault_initialization(self, tmp_path):
        vault_file = tmp_path / "test.vault"
        vault = PasswordVault("testmaster", vault_file=vault_file)
        assert vault is not None
        assert vault.master_password == "testmaster"
        assert vault.vault_file == vault_file
    
    def test_add_password_and_round_trip(self, tmp_path):
        vault_file = tmp_path / "test.vault"
        vault = PasswordVault("testmaster", vault_file=vault_file)
        vault.add("gmail", "user@example.com", "password123")
        
        assert len(vault.entries) == 1
        assert vault.entries[0].site == "gmail"
        
        # Test loading from the same file
        vault2 = PasswordVault("testmaster", vault_file=vault_file)
        assert len(vault2.entries) == 1
        assert vault2.entries[0].site == "gmail"
        assert vault2.entries[0].password == "password123"

    def test_wrong_password_rejected(self, tmp_path):
        vault_file = tmp_path / "test.vault"
        vault = PasswordVault("correct_password", vault_file=vault_file)
        vault.add("gmail", "user", "pass")

        # Wrong password must fail GCM authentication with an explicit error,
        # not silently load an empty vault.
        with pytest.raises(VaultError):
            PasswordVault("wrong_password", vault_file=vault_file)

    def test_tampered_file_detected(self, tmp_path):
        vault_file = tmp_path / "test.vault"
        vault = PasswordVault("correct_password", vault_file=vault_file)
        vault.add("gmail", "user", "pass")

        # Tamper with the encrypted content
        encrypted = vault_file.read_bytes()
        tampered = encrypted[:-1] + (b"a" if encrypted[-1] != ord("a") else b"b")
        vault_file.write_bytes(tampered)

        # GCM auth failure must surface as an explicit error, not silent data.
        with pytest.raises(VaultError):
            PasswordVault("correct_password", vault_file=vault_file)


class TestCrypto:
    def test_vault_encrypt_decrypt_round_trip(self):
        plaintext = b"secret_data"
        master_password = "correct horse battery staple"
        encrypted = vault_encrypt(plaintext, master_password)
        assert encrypted != plaintext
        assert vault_decrypt(encrypted, master_password) == plaintext

    def test_vault_encrypt_wrong_password_rejected(self):
        plaintext = b"secret_data"
        encrypted = vault_encrypt(plaintext, "right_password")
        with pytest.raises(VaultError):
            vault_decrypt(encrypted, "wrong_password")

    def test_vault_encrypt_not_tamper_evident(self):
        plaintext = b"secret_data"
        master_password = "correct horse battery staple"
        encrypted = bytearray(vault_encrypt(plaintext, master_password))
        encrypted[-1] ^= 0xFF  # flip a bit in the ciphertext
        with pytest.raises(VaultError):
            vault_decrypt(bytes(encrypted), master_password)

    def test_vault_encrypt_invalid_header_rejected(self):
        with pytest.raises(VaultError):
            vault_decrypt(b"garbage-not-a-vault", "key")


class TestMainApp:
    @patch('curses.wrapper')
    def test_main_cli_instantiation(self, mock_wrapper):
        from vault import main
        
        main()
        mock_wrapper.assert_called_once()
        
        wrapper_arg = mock_wrapper.call_args[0][0]
        assert callable(wrapper_arg)
        
        with patch('vault.PasswordManagerCLI') as MockCLI:
            mock_stdscr = Mock()
            wrapper_arg(mock_stdscr)
            MockCLI.assert_called_once_with(mock_stdscr)
            MockCLI.return_value.run.assert_called_once()
