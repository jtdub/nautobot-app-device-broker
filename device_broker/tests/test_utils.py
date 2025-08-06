"""Test module for device broker utilities and driver functionality."""

import unittest
from unittest.mock import MagicMock, patch

from device_broker.utils import get_platform_driver


class TestDeviceBrokerNetmikoDriver(unittest.TestCase):
    """Test cases for device broker Netmiko driver functionality."""

    @patch("netmiko.ConnectHandler")
    def test_platform_network_driver_happy_path(self, mock_connect_handler):
        # Prepare mock Netmiko connection instance
        mock_conn = MagicMock()
        mock_connect_handler.return_value = mock_conn

        # Prepare mock Nautobot Platform model
        class MockPlatform:  # pylint: disable=too-few-public-methods
            """Mock platform class for testing with network_driver attribute."""

            network_driver = "cisco_ios"

        creds = {"username": "admin", "password": "passw0rd"}
        platform = MockPlatform()
        host = "10.1.1.1"
        commands = ["show version", "show run"]

        # Test get_platform_driver
        driver = get_platform_driver(platform)
        self.assertIsNotNone(driver)
        # Test connect
        connection = driver.connect(host, creds)
        self.assertIs(connection.connection, mock_conn)
        # Test send_command
        mock_conn.send_command.return_value = "SHOW VER OUTPUT"
        output = connection.send_command(commands[0])
        mock_conn.send_command.assert_called_with(commands[0])
        self.assertEqual(output, "SHOW VER OUTPUT")
        # Test config mode
        connection.enter_config_mode()
        mock_conn.config_mode.assert_called_once()
        # Test disconnect
        connection.disconnect()
        mock_conn.disconnect.assert_called_once()

    def test_platform_missing_or_blank_network_driver(self):
        # Platform with 'network_driver' as None
        class PlatformNone:  # pylint: disable=too-few-public-methods
            """Mock platform class with None network_driver for testing."""

            network_driver = None

        driver = get_platform_driver(PlatformNone())
        self.assertIsNone(driver)

        # Platform with no 'network_driver' attribute
        class PlatformNoAttr:  # pylint: disable=too-few-public-methods
            """Mock platform class without network_driver attribute for testing."""

        driver2 = get_platform_driver(PlatformNoAttr())
        self.assertIsNone(driver2)

        # Platform with blank 'network_driver'
        class PlatformBlank:  # pylint: disable=too-few-public-methods
            """Mock platform class with empty network_driver for testing."""

            network_driver = ""

        driver3 = get_platform_driver(PlatformBlank())
        self.assertIsNone(driver3)
