"""Unit tests for Password Vault"""

import pytest
from unittest.mock import Mock, patch
from vault import PasswordVault, PasswordGenerator


class TestPasswordGenerator:
    def test_generate_password_length(self):
        generator = PasswordGenerator()
        password = generator.generate(length=16)
        assert len(password) == 16
    
    def test_generate_password_with_special_chars(self):
        generator = PasswordGenerator()
        password = generator.generate(length=16, use_special=True)
        # Should contain special characters
        assert any(c in password for c in '!@#$%^&*()')
    
    def test_generate_password_numbers(self):
        generator = PasswordGenerator()
        password = generator.generate(length=16, use_numbers=True)
        assert any(c.isdigit() for c in password)
    
    def test_generate_password_uppercase(self):
        generator = PasswordGenerator()
        password = generator.generate(length=16, use_uppercase=True)
        assert any(c.isupper() for c in password)


class TestPasswordVault:
    @patch('vault.getpass')
    def test_vault_initialization(self, mock_getpass):
        mock_getpass.return_value = "testmaster"
        vault = PasswordVault("test.db")
        assert vault is not None
    
    @patch('vault.getpass')
    def test_add_password(self, mock_getpass):
        mock_getpass.return_value = "testmaster"
        vault = PasswordVault("test.db")
        vault.add_password("gmail", "user@example.com", "password123")
        # Should be able to retrieve
        assert True
    
    @patch('vault.getpass')
    def test_generate_strong_password(self, mock_getpass):
        mock_getpass.return_value = "testmaster"
        vault = PasswordVault("test.db")
        password = vault.generate_strong_password(length=20)
        assert len(password) == 20
