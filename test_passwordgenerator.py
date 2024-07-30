import unittest
from tkinter import Tk, Entry, Button
from tkinter import messagebox
from random import randint
from unittest.mock import patch, MagicMock

class TestPasswordGenerator(unittest.TestCase):

    def setUp(self):
        self.tk = Tk()
        self.my_entry = Entry(self.tk)
        self.pw_entry = Entry(self.tk)
        self.pw_length = 10  # Example password length for tests

    def test_password_generation(self):
        # Test the length and type of the generated password
        generated_pw = self.generate_password(self.pw_length)
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
        generated_pw = self.generate_password(0)
        self.assertEqual(generated_pw, "", "Generated password should be an empty string when length is zero")

    def test_large_password_generation(self):
        # Test generating a very large password
        length = 1000
        generated_pw = self.generate_password(length)
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

    def generate_password(self, length):
        password = ''
        for _ in range(length):
            password += chr(randint(33, 126))
        return password

    def copy_to_clipboard(self, text):
        self.tk.clipboard_clear()
        self.tk.clipboard_append(text)
        messagebox.showinfo("Success", "Text copied to clipboard!")

    def tearDown(self):
        self.tk.destroy()

if __name__ == "__main__":
    unittest.main()
