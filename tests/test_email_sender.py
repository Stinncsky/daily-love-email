"""Tests for email_sender module."""
import unittest
from unittest.mock import patch, Mock
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import email_sender


class TestEmailSender(unittest.TestCase):
    """Test cases for send_email function."""

    @patch('email_sender.smtplib.SMTP_SSL')
    def test_send_email_success_with_sender_name(self, mock_smtp_ssl):
        """Test successful email sending with sender name."""
        config = {
            'smtp_server': 'smtp.example.com',
            'smtp_port': 465,
            'smtp_user': 'user@example.com',
            'smtp_password': 'secret',
            'from_email': 'from@example.com',
            'sender_name': 'SenderName',
            'to_email': 'to@example.com'
        }
        
        # Setup mock
        mock_server = Mock()
        mock_smtp_ssl.return_value.__enter__ = Mock(return_value=mock_server)
        mock_smtp_ssl.return_value.__exit__ = Mock(return_value=False)
        mock_server.login.return_value = (235, b'Authentication successful')
        mock_server.sendmail.return_value = {}
        
        result = email_sender.send_email(config, 'Test Subject', '<p>Hi</p>', to='recipient@example.org')
        
        self.assertTrue(result)
        mock_smtp_ssl.assert_called_once()
        mock_server.login.assert_called_once_with('user@example.com', 'secret')
        mock_server.sendmail.assert_called_once()

    @patch('email_sender.smtplib.SMTP_SSL')
    def test_send_email_missing_recipient(self, mock_smtp_ssl):
        """Test that missing recipient returns False."""
        config = {
            'smtp_server': 'smtp.example.com',
            'smtp_port': 465,
            'smtp_user': 'user@example.com',
            'smtp_password': 'secret',
            'from_email': 'from@example.com',
            'to_email': None
        }
        
        result = email_sender.send_email(config, 'Subject', '<p>Hi</p>', to=None)
        
        self.assertFalse(result)
        mock_smtp_ssl.assert_not_called()

    @patch('email_sender.smtplib.SMTP_SSL')
    def test_send_email_smtp_connection_failure(self, mock_smtp_ssl):
        """Test handling of SMTP connection failure."""
        config = {
            'smtp_server': 'smtp.example.com',
            'smtp_port': 465,
            'smtp_user': 'user@example.com',
            'smtp_password': 'secret',
            'from_email': 'from@example.com',
            'to_email': 'to@example.com'
        }
        
        mock_smtp_ssl.side_effect = Exception('Connection failed')
        
        result = email_sender.send_email(config, 'Subject', '<p>Hi</p>')
        
        self.assertFalse(result)

    @patch('email_sender.smtplib.SMTP_SSL')
    def test_send_email_without_sender_name(self, mock_smtp_ssl):
        """Test email sending without sender name uses from_email."""
        config = {
            'smtp_server': 'smtp.example.com',
            'smtp_port': 465,
            'smtp_user': 'user@example.com',
            'smtp_password': 'secret',
            'from_email': 'from@example.com',
            'to_email': 'to@example.com'
        }
        
        # Setup mock
        mock_server = Mock()
        mock_smtp_ssl.return_value.__enter__ = Mock(return_value=mock_server)
        mock_smtp_ssl.return_value.__exit__ = Mock(return_value=False)
        mock_server.login.return_value = (235, b'OK')
        mock_server.sendmail.return_value = {}
        
        result = email_sender.send_email(config, 'Subject', '<p>Hi</p>')
        
        self.assertTrue(result)
        mock_server.sendmail.assert_called_once()


if __name__ == '__main__':
    unittest.main()
