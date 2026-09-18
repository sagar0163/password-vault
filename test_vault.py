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
        password = generator.generate(length=16, symbols=True)
        # Should contain special characters
        assert any(c in password for c in '!@#$%^&*()_+-=[]{}|;:,.<>?')
    
    def test_generate_password_numbers(self):
        generator = PasswordGenerator()
        password = generator.generate(length=16, digits=True)
        assert any(c.isdigit() for c in password)
    
    def test_generate_password_uppercase(self):
        generator = PasswordGenerator()
        password = generator.generate(length=16, uppercase=True)
        assert any(c.isupper() for c in password)


class TestPasswordVault:
    def test_vault_initialization(self):
        vault = PasswordVault("testmaster")
        assert vault is not None
        assert vault.master_password == "testmaster"
    
    def test_add_password(self):
        vault = PasswordVault("testmaster")
        vault.add("gmail", "user@example.com", "password123")
        # Should be able to retrieve
        assert len(vault.entries) > 0
        assert vault.entries[0].site == "gmail"
        
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


