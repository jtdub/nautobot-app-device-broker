"""Test module for device broker utilities and driver functionality."""

import unittest
from unittest.mock import MagicMock, patch

from netmiko import ConnectHandler

# Assume your driver code is in drivers.py, example:
# from drivers import get_platform_driver

# For this example, let's include the function directly:
PLATFORM_TO_NETMIKO = {
    "cisco_ios": "cisco_ios",
}


class NetmikoDriverWrapper:  # pylint: disable=duplicate-code
    """Test wrapper class for Netmiko connections."""

    def __init__(self, device_type, host, credentials):
        """Initialize the test driver wrapper.

        Args:
            device_type: Netmiko device type identifier
            host: Target device hostname or IP address
            credentials: Dictionary containing authentication credentials
        """
        self.device_type = device_type
        self.host = host
        self.credentials = credentials
        self.connection = None

    def connect(self):
        """Establish connection to the network device.

        Returns:
            NetmikoDriverWrapper: Self-reference for method chaining
        """
        params = {
            "device_type": self.device_type,
            "host": self.host,
            "username": self.credentials.get("username"),
            "password": self.credentials.get("password"),
        }
        self.connection = ConnectHandler(**params)
        return self

    def enter_config_mode(self):
        """Enter configuration mode on the device."""
        self.connection.config_mode()

    def send_command(self, cmd):
        """Send a command to the device and return the output.

        Args:
            cmd: Command string to execute

        Returns:
            str: Command output from the device
        """
        return self.connection.send_command(cmd)

    def disconnect(self):
        """Disconnect from the network device."""
        self.connection.disconnect()


def get_platform_driver(platform_slug):  # pylint: disable=duplicate-code
    """Get the appropriate driver for a given platform slug.

    Args:
        platform_slug: Nautobot platform slug identifier

    Returns:
        type or None: Driver class if platform is supported, None otherwise
    """
    device_type = PLATFORM_TO_NETMIKO.get(platform_slug)
    if not device_type:
        return None

    def driver_factory(host, credentials):
        wrapper = NetmikoDriverWrapper(device_type, host, credentials)
        return wrapper.connect()

    return type("DynamicDriver", (), {"connect": staticmethod(driver_factory)})


class TestDeviceBrokerDriver(unittest.TestCase):
    """Test cases for device broker driver functionality."""

    @patch("netmiko.ConnectHandler")
    def test_get_platform_driver_and_commands(self, mock_connect_handler):
        """Test driver creation and command execution functionality."""
        # Mock Netmiko connection & methods
        mock_conn = MagicMock()
        mock_connect_handler.return_value = mock_conn

        # Example device info
        creds = {"username": "admin", "password": "passw0rd"}
        platform_slug = "cisco_ios"
        host = "10.1.1.1"
        commands = ["show version", "show ip int brief"]

        # Setup driver
        driver = get_platform_driver(platform_slug)
        self.assertIsNotNone(driver)

        # Simulate connection
        connection = driver.connect(host, creds)
        self.assertIsInstance(connection, NetmikoDriverWrapper)
        self.assertIs(connection.connection, mock_conn)

        # Simulate command execution
        mock_conn.send_command.return_value = "VERSION OUTPUT"
        output = connection.send_command(commands[0])
        mock_conn.send_command.assert_called_with(commands[0])
        self.assertEqual(output, "VERSION OUTPUT")

        # Simulate config mode
        connection.enter_config_mode()
        mock_conn.config_mode.assert_called_once()

        # Simulate disconnect
        connection.disconnect()
        mock_conn.disconnect.assert_called_once()

    def test_get_platform_driver_invalid_platform(self):
        """Test that invalid platform returns None."""
        driver = get_platform_driver("unknown_platform")
        self.assertIsNone(driver)
