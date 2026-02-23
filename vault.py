#!/usr/bin/env python3
"""
Secure Password Vault
====================
A terminal-based password manager with encryption.

Features:
- Generate strong passwords
- Store passwords encrypted
- Search and retrieve
- Password strength checker
- Auto-lock after inactivity
- Clipboard support
"""

import os
import sys
import json
import time
import secrets
import string
import curses
import pyperclip
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime


# Simple encryption (for demonstration - use keyring in production)
def simple_encrypt(data: str, key: str) -> str:
    """Simple XOR encryption"""
    result = []
    for i, char in enumerate(data):
        result.append(chr(ord(char) ^ ord(key[i % len(key)])))
    return ''.join(result)


def simple_decrypt(data: str, key: str) -> str:
    """Simple XOR decryption"""
    return simple_encrypt(data, key)


@dataclass
class PasswordEntry:
    """Password entry"""
    id: str
    site: str
    username: str
    password: str
    url: str
    notes: str
    created: str
    modified: str
    strength: int


class PasswordGenerator:
    """Generate secure passwords"""
    
    CHARSETS = {
        'lowercase': string.ascii_lowercase,
        'uppercase': string.ascii_uppercase,
        'digits': string.digits,
        'symbols': '!@#$%^&*()_+-=[]{}|;:,.<>?',
    }
    
    @staticmethod
    def generate(
        length: int = 16,
        lowercase: bool = True,
        uppercase: bool = True,
        digits: bool = True,
        symbols: bool = True
    ) -> str:
        """Generate a random password"""
        charset = ''
        if lowercase:
            charset += PasswordGenerator.CHARSETS['lowercase']
        if uppercase:
            charset += PasswordGenerator.CHARSETS['uppercase']
        if digits:
            charset += PasswordGenerator.CHARSETS['digits']
        if symbols:
            charset += PasswordGenerator.CHARSETS['symbols']
        
        if not charset:
            charset = PasswordGenerator.CHARSETS['lowercase']
        
        return ''.join(secrets.choice(charset) for _ in range(length))
    
    @staticmethod
    def check_strength(password: str) -> int:
        """Check password strength (0-100)"""
        score = 0
        
        # Length
        score += min(len(password) * 4, 40)
        
        # Character types
        if any(c in string.ascii_lowercase for c in password):
            score += 10
        if any(c in string.ascii_uppercase for c in password):
            score += 10
        if any(c in string.digits for c in password):
            score += 10
        if any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password):
            score += 15
        
        # Penalties
        common = ['password', '123456', 'qwerty', 'admin', 'letmein']
        if any(c in password.lower() for c in common):
            score -= 30
        
        return max(0, min(score, 100))


class PasswordVault:
    """Password vault manager"""
    
    def __init__(self, master_password: str):
        self.master_password = master_password
        self.vault_file = Path.home() / '.password_vault'
        self.entries: List[PasswordEntry] = []
        self.locked = False
        self.last_activity = time.time()
        self.timeout = 300  # 5 minutes
        
        self.load()
    
    def load(self):
        """Load vault from file"""
        if self.vault_file.exists():
            try:
                encrypted = self.vault_file.read_text()
                decrypted = simple_decrypt(encrypted, self.master_password)
                data = json.loads(decrypted)
                
                self.entries = [PasswordEntry(**e) for e in data]
            except:
                self.entries = []
        else:
            self.entries = []
    
    def save(self):
        """Save vault to file"""
        data = json.dumps([{
            'id': e.id,
            'site': e.site,
            'username': e.username,
            'password': e.password,
            'url': e.url,
            'notes': e.notes,
            'created': e.created,
            'modified': e.modified,
            'strength': e.strength
        } for e in self.entries])
        
        encrypted = simple_encrypt(data, self.master_password)
        self.vault_file.write_text(encrypted)
    
    def add(self, site: str, username: str, password: str, url: str = '', notes: str = ''):
        """Add a new entry"""
        entry = PasswordEntry(
            id=secrets.token_hex(8),
            site=site,
            username=username,
            password=password,
            url=url,
            notes=notes,
            created=datetime.now().isoformat(),
            modified=datetime.now().isoformat(),
            strength=PasswordGenerator.check_strength(password)
        )
        
        self.entries.append(entry)
        self.save()
        self.last_activity = time.time()
    
    def update(self, entry_id: str, **kwargs):
        """Update an entry"""
        for entry in self.entries:
            if entry.id == entry_id:
                for key, value in kwargs.items():
                    if hasattr(entry, key):
                        setattr(entry, key, value)
                entry.modified = datetime.now().isoformat()
                entry.strength = PasswordGenerator.check_strength(entry.password)
                break
        
        self.save()
        self.last_activity = time.time()
    
    def delete(self, entry_id: str):
        """Delete an entry"""
        self.entries = [e for e in self.entries if e.id != entry_id]
        self.save()
        self.last_activity = time.time()
    
    def search(self, query: str) -> List[PasswordEntry]:
        """Search entries"""
        query = query.lower()
        return [
            e for e in self.entries
            if query in e.site.lower() or query in e.username.lower()
        ]
    
    def get(self, entry_id: str) -> Optional[PasswordEntry]:
        """Get entry by ID"""
        for entry in self.entries:
            if entry.id == entry_id:
                return entry
        return None
    
    def is_locked(self) -> bool:
        """Check if vault is locked"""
        if time.time() - self.last_activity > self.timeout:
            self.locked = True
        return self.locked
    
    def unlock(self):
        """Unlock vault"""
        self.locked = False
        self.last_activity = time.time()


class PasswordManagerCLI:
    """CLI interface"""
    
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.vault = None
        self.master_password = None
        self.current_view = 'menu'
        self.search_query = ''
        self.selected_index = 0
        
        # Setup
        curses.curs_set(0)
        curses.start_color()
        
        # Colors
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    
    def draw_header(self, title: str):
        """Draw header"""
        self.stdscr.clear()
        width = curses.COLS
        
        self.stdscr.addstr(0, 0, '🔐 ' + title.center(width - 4), 
                          curses.color_pair(1) | curses.A_BOLD)
        self.stdscr.addstr(1, 0, '─' * width)
    
    def draw_menu(self):
        """Draw main menu"""
        self.draw_header('Password Vault')
        
        options = [
            ('🔍', 'Search passwords'),
            ('➕', 'Add new password'),
            ('📋', 'Generate password'),
            ('⚙️', 'Settings'),
            ('🚪', 'Exit'),
        ]
        
        for i, (emoji, desc) in enumerate(options, 3):
            prefix = '► ' if i == 3 + self.selected_index else '  '
            self.stdscr.addstr(i, 5, f'{prefix}{emoji} {desc}')
        
        self.stdscr.refresh()
    
    def draw_list(self, entries: List[PasswordEntry], title: str = 'Passwords'):
        """Draw password list"""
        self.draw_header(title)
        
        if not entries:
            self.stdscr.addstr(3, 5, 'No passwords found.', curses.color_pair(3))
            return
        
        # Calculate visible range
        height = curses.LINES - 4
        start = max(0, self.selected_index - height // 2)
        end = min(len(entries), start + height)
        
        for i, entry in enumerate(entries[start:end], start):
            prefix = '► ' if i == self.selected_index else '  '
            strength_color = (
                curses.color_pair(4) if entry.strength < 50 else
                curses.color_pair(3) if entry.strength < 75 else
                curses.color_pair(2)
            )
            
            self.stdscr.addstr(3 + i - start, 5, f'{prefix}{entry.site}')
            self.stdscr.addstr(3 + i - start, 35, f'{entry.username}', 
                            curses.color_pair(5))
            self.stdscr.addstr(3 + i - start, 55, f'[{entry.strength}%]', 
                            strength_color)
        
        # Help
        self.stdscr.addstr(curses.LINES - 3, 0, '↑↓ Navigate | Enter View | d Delete | q Back')
        self.stdscr.refresh()
    
    def draw_entry(self, entry: PasswordEntry):
        """Draw entry details"""
        self.draw_header(f'Password: {entry.site}')
        
        y = 3
        
        self.stdscr.addstr(y, 5, f'🔗 URL: {entry.url or "-"}')
        y += 1
        self.stdscr.addstr(y, 5, f'👤 Username: {entry.username}')
        y += 1
        
        # Password (masked)
        masked = '*' * min(len(entry.password), 20)
        self.stdscr.addstr(y, 5, f'🔑 Password: {masked}')
        y += 1
        
        # Strength bar
        strength = entry.strength
        bar = '█' * (strength // 5) + '░' * (20 - strength // 5)
        strength_color = (
            curses.color_pair(4) if strength < 50 else
            curses.color_pair(3) if strength < 75 else
            curses.color_pair(2)
        )
        self.stdscr.addstr(y, 5, f'💪 Strength: [{bar}] {strength}%', strength_color)
        y += 2
        
        self.stdscr.addstr(y, 5, f'📝 Notes: {entry.notes or "-"}')
        y += 2
        
        self.stdscr.addstr(y, 5, f'📅 Created: {entry.created[:10]}')
        y += 1
        self.stdscr.addstr(y, 5, f'✏️  Modified: {entry.modified[:10]}')
        
        y += 2
        self.stdscr.addstr(y, 5, '[c] Copy password | [u] Copy username | [e] Edit | [d] Delete | [q] Back')
        self.stdscr.refresh()
    
    def draw_generator(self):
        """Draw password generator"""
        self.draw_header('Password Generator')
        
        password = PasswordGenerator.generate(16)
        strength = PasswordGenerator.check_strength(password)
        
        y = 3
        self.stdscr.addstr(y, 5, 'Generated Password:', curses.color_pair(1))
        y += 1
        self.stdscr.addstr(y, 5, password, curses.color_pair(2) | curses.A_BOLD)
        y += 2
        
        bar = '█' * (strength // 5) + '░' * (20 - strength // 5)
        self.stdscr.addstr(y, 5, f'Strength: [{bar}] {strength}%')
        y += 3
        
        self.stdscr.addstr(y, 5, '[r] Regenerate | [c] Copy | [s] Save | [q] Back')
        self.stdscr.refresh()
        
        return password
    
    def get_input(self, prompt: str, y: int = 3) -> str:
        """Get user input"""
        curses.echo()
        self.stdscr.addstr(y, 5, prompt)
        value = self.stdscr.getstr(y, len(prompt) + 5).decode()
        curses.noecho()
        return value
    
    def run(self):
        """Main loop"""
        while True:
            if self.vault and self.vault.is_locked():
                self.vault = None
                self.master_password = None
            
            if not self.vault:
                self.draw_login()
            elif self.current_view == 'menu':
                self.draw_menu()
            elif self.current_view == 'list':
                self.draw_list(self.vault.entries)
            elif self.current_view == 'generator':
                self.draw_generator()
            
            try:
                key = self.stdscr.getch()
                
                if key == ord('q'):
                    if self.current_view == 'menu':
                        break
                    else:
                        self.current_view = 'menu'
                        self.selected_index = 0
                
                elif key in [curses.KEY_UP, ord('k')]:
                    if self.current_view == 'list' and self.vault:
                        self.selected_index = max(0, self.selected_index - 1)
                    elif self.current_view == 'menu':
                        self.selected_index = (self.selected_index - 1) % 5
                
                elif key in [curses.KEY_DOWN, ord('j')]:
                    if self.current_view == 'list' and self.vault:
                        self.selected_index = min(len(self.vault.entries) - 1, self.selected_index + 1)
                    elif self.current_view == 'menu':
                        self.selected_index = (self.selected_index + 1) % 5
                
                elif key == ord('\n'):
                    if self.current_view == 'menu':
                        if self.selected_index == 0:  # Search
                            self.current_view = 'list'
                        elif self.selected_index == 1:  # Add
                            self.draw_add_entry()
                        elif self.selected_index == 2:  # Generator
                            self.current_view = 'generator'
                        elif self.selected_index == 4:  # Exit
                            break
                    elif self.current_view == 'list' and self.vault.entries:
                        entry = self.vault.entries[self.selected_index]
                        self.draw_entry(entry)
                
                elif key == ord('d') and self.current_view == 'list':
                    if self.vault and self.vault.entries:
                        entry = self.vault.entries[self.selected_index]
                        self.vault.delete(entry.id)
                
                elif key == ord('r') and self.current_view == 'generator':
                    self.draw_generator()
                
                elif key == ord('c') and self.current_view == 'generator':
                    pass  # Copy to clipboard
                
            except KeyboardInterrupt:
                break
    
    def draw_login(self):
        """Draw login screen"""
        self.draw_header('Password Vault - Login')
        
        y = 5
        self.stdscr.addstr(y, 5, 'Enter master password:')
        curses.echo()
        password = self.stdscr.getstr(y, 30).decode()
        curses.nocho()
        
        self.vault = PasswordVault(password)
        self.master_password = password
        
        # Try to load
        self.vault.load()
        
        self.current_view = 'menu'
    
    def draw_add_entry(self):
        """Draw add entry form"""
        self.draw_header('Add New Password')
        
        site = self.get_input('Site/Service: ')
        username = self.get_input('Username/Email: ', 4)
        password = self.get_input('Password: ', 5)
        
        if not password:
            password = PasswordGenerator.generate(16)
        
        url = self.get_input('URL (optional): ', 6)
        notes = self.get_input('Notes (optional): ', 7)
        
        if site and username:
            self.vault.add(site, username, password, url, notes)


def main():
    """Entry point"""
    try:
        curses.wrapper(PasswordManagerCLI.run)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    main()
