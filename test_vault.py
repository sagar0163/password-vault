"""Unit tests for Password Vault"""

import pytest
import json
from unittest.mock import Mock, patch
from pathlib import Path
from vault import PasswordVault, PasswordGenerator, simple_encrypt, simple_decrypt


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
        
        # When trying to load with wrong password, JSON decoding will fail and it should load an empty vault
        vault_wrong = PasswordVault("wrong_password", vault_file=vault_file)
        assert len(vault_wrong.entries) == 0

    def test_tampered_file_detected(self, tmp_path):
        vault_file = tmp_path / "test.vault"
        vault = PasswordVault("correct_password", vault_file=vault_file)
        vault.add("gmail", "user", "pass")

        # Tamper with the encrypted content
        encrypted = vault_file.read_text()
        tampered = encrypted[:-1] + ("a" if encrypted[-1] != "a" else "b")
        vault_file.write_text(tampered)

        vault_tampered = PasswordVault("correct_password", vault_file=vault_file)
        # Should catch JSONDecodeError or similar during decryption/loading and reset entries to []
        assert len(vault_tampered.entries) == 0


class TestCrypto:
    def test_simple_encrypt_decrypt(self):
        plaintext = "secret_data"
        key = "my_key"
        encrypted = simple_encrypt(plaintext, key)
        assert encrypted != plaintext
        decrypted = simple_decrypt(encrypted, key)
        assert decrypted == plaintext


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
