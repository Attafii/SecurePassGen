import unittest
from tkinter import Tk, Entry, Button, Label, StringVar, BooleanVar, Checkbutton, messagebox
from unittest.mock import patch, MagicMock
from random import randint, choice, shuffle

class TestPasswordGenerator(unittest.TestCase):

    def setUp(self):
        self.tk = Tk()
        self.my_entry = Entry(self.tk)
        self.pw_entry = Entry(self.tk)
        self.strength_text = StringVar()
        self.strength_label = Label(self.tk, textvariable=self.strength_text)
        self.var_uppercase = BooleanVar(value=True)
        self.var_lowercase = BooleanVar(value=True)
        self.var_numbers = BooleanVar(value=True)
        self.var_special = BooleanVar(value=True)
        
        # Initialize UI elements for testing
        self.my_entry.pack()
        self.pw_entry.pack()
        self.strength_label.pack()

        # Checkbuttons for character types
        Checkbutton(self.tk, text="Uppercase Letters (A-Z)", variable=self.var_uppercase).pack(anchor='w')
        Checkbutton(self.tk, text="Lowercase Letters (a-z)", variable=self.var_lowercase).pack(anchor='w')
        Checkbutton(self.tk, text="Numbers (0-9)", variable=self.var_numbers).pack(anchor='w')
        Checkbutton(self.tk, text="Special Characters (!@#$%^&*)", variable=self.var_special).pack(anchor='w')
        
        self.pw_length = 10  # Example password length for tests

    def generate_password(self, length, use_uppercase, use_lowercase, use_numbers, use_special):
        char_types = []
        if use_uppercase:
            char_types.append('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        if use_lowercase:
            char_types.append('abcdefghijklmnopqrstuvwxyz')
        if use_numbers:
            char_types.append('0123456789')
        if use_special:
            char_types.append('!@#$%^&*()-_=+[]{}|;:,.<>?/')

        my_password = []
        while len(my_password) < length:
            char_list = choice(char_types)
            my_password.append(choice(char_list))

        shuffle(my_password)
        return ''.join(my_password[:length])

    def test_password_includes_selected_characters(self):
        # Test case where all character types are selected
        self.var_uppercase.set(True)
        self.var_lowercase.set(True)
        self.var_numbers.set(True)
        self.var_special.set(True)
        generated_pw = self.generate_password(self.pw_length, True, True, True, True)
        self.assertTrue(any(c.isupper() for c in generated_pw), "Password should include uppercase letters")
        self.assertTrue(any(c.islower() for c in generated_pw), "Password should include lowercase letters")
        self.assertTrue(any(c.isdigit() for c in generated_pw), "Password should include numbers")
        self.assertTrue(any(c in '!@#$%^&*()-_=+[]{}|;:,.<>?/' for c in generated_pw), "Password should include special characters")

    def test_password_excludes_unselected_characters(self):
        # Test case where only lowercase letters are selected
        self.var_uppercase.set(False)
        self.var_lowercase.set(True)
        self.var_numbers.set(False)
        self.var_special.set(False)
        generated_pw = self.generate_password(self.pw_length, False, True, False, False)
        self.assertTrue(all(c.islower() for c in generated_pw), "Password should only include lowercase letters")
        self.assertFalse(any(c.isupper() for c in generated_pw), "Password should not include uppercase letters")
        self.assertFalse(any(c.isdigit() for c in generated_pw), "Password should not include numbers")
        self.assertFalse(any(c in '!@#$%^&*()-_=+[]{}|;:,.<>?/' for c in generated_pw), "Password should not include special characters")

    def test_password_generation(self):
        # Test the length and type of the generated password
        generated_pw = self.generate_password(self.pw_length, True, True, True, True)
        self.assertEqual(len(generated_pw), self.pw_length, "Generated password length should match input length")
        self.assertIsInstance(generated_pw, str, "Generated password should be a string")

    def test_clipboard_copy(self):
        # Test the clipboard copy functionality
        with patch.object(self.tk, 'clipboard_clear') as mock_clear:
            with patch.object(self.tk, 'clipboard_append') as mock_append:
                self.copy_to_clipboard("test_password")
                mock_clear.assert_called_once()
                mock_append.assert_called_once_with("test_password")

    def test_empty_password_generation(self):
        # Test edge case where password length is zero
        generated_pw = self.generate_password(0, True, True, True, True)
        self.assertEqual(generated_pw, "", "Generated password should be an empty string when length is zero")

    def test_large_password_generation(self):
        # Test generating a very large password
        length = 1000
        generated_pw = self.generate_password(length, True, True, True, True)
        self.assertEqual(len(generated_pw), length, "Generated password length should match the large input length")

    def test_clipboard_copy_empty_text(self):
        # Test copying an empty string to the clipboard
        with patch.object(self.tk, 'clipboard_clear') as mock_clear:
            with patch.object(self.tk, 'clipboard_append') as mock_append:
                self.copy_to_clipboard("")
                mock_clear.assert_called_once()
                mock_append.assert_called_once_with("")

    def test_messagebox_showinfo_called(self):
        # Test if the messagebox is shown when copying to clipboard
        with patch('tkinter.messagebox.showinfo') as mock_showinfo:
            self.copy_to_clipboard("test_password")
            mock_showinfo.assert_called_once_with("Success", "Text copied to clipboard!")

    def evaluate_strength(self, password):
        # Mock implementation for testing
        pass

    def copy_to_clipboard(self, text):
        self.tk.clipboard_clear()
        self.tk.clipboard_append(text)
        messagebox.showinfo("Success", "Text copied to clipboard!")

    def tearDown(self):
        self.tk.destroy()

if __name__ == "__main__":
    unittest.main()
