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
    @patch('vault.Path.home')
    def test_vault_initialization(self, mock_home, tmp_path):
        mock_home.return_value = tmp_path
        vault = PasswordVault("testmaster")
        assert vault is not None
        assert vault.master_password == "testmaster"
    
    @patch('vault.Path.home')
    def test_add_password(self, mock_home, tmp_path):
        mock_home.return_value = tmp_path
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



    @patch('vault.Path.home')
    def test_wrong_password_rejected(self, mock_home, tmp_path):
        mock_home.return_value = tmp_path
        vault = PasswordVault("testmaster")
        vault.add("gmail", "user", "pass")
        
        # Now try to load with wrong password
        with pytest.raises(ValueError, match="Invalid master password or corrupted vault"):
            PasswordVault("wrongpassword")

    @patch('vault.Path.home')
    def test_no_vault_mutation_on_wrong_password(self, mock_home, tmp_path):
        mock_home.return_value = tmp_path
        vault1 = PasswordVault("correct")
        vault1.add("gmail", "user", "pass")
        
        # File should be modified
        original_content = (tmp_path / '.password_vault').read_text()
        
        # Try wrong password
        with pytest.raises(ValueError):
            PasswordVault("wrong")
            
        # File should remain exactly the same
        assert (tmp_path / '.password_vault').read_text() == original_content

    @patch('vault.Path.home')
    def test_save_atomic_and_permissions(self, mock_home, tmp_path):
        mock_home.return_value = tmp_path
        vault = PasswordVault("testmaster")
        vault.add("gmail", "user", "pass")
        
        vault_file = tmp_path / '.password_vault'
        assert vault_file.exists()
        
        # Check permissions (0o600)
        import os
        import stat
        st = os.stat(vault_file)
        # We check if owner has read and write, and others have nothing.
        # st.st_mode & 0o777 should be 0o600
        assert stat.S_IMODE(st.st_mode) == 0o600

    @patch('vault.Path.home')
    def test_first_run_creates_vault(self, mock_home, tmp_path):
        mock_home.return_value = tmp_path
        vault = PasswordVault("testmaster")
        assert len(vault.entries) == 0
        vault.add("gmail", "user", "pass")
        assert (tmp_path / '.password_vault').exists()
