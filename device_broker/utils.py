"""Device Broker utilities for network device platform drivers and connections."""

from netmiko import ConnectHandler


class NetmikoDriverWrapper:
    """Wrapper class for Netmiko connection handling with device platforms."""

    def __init__(self, device_type, host, credentials):
        """Initialize the NetmikoDriverWrapper with connection parameters.

        Args:
            device_type (str): The Netmiko device type identifier.
            host (str): The host IP address or hostname.
            credentials (dict): Dictionary containing username and password.
        """
        self.device_type = device_type
        self.host = host
        self.credentials = credentials
        self.connection = None

    def connect(self):
        """Establish connection to the network device using Netmiko.

        Returns:
            NetmikoDriverWrapper: Returns self for method chaining.
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
        """Enter configuration mode on the network device."""
        self.connection.config_mode()

    def send_command(self, cmd):
        """Send a command to the network device and return the output.

        Args:
            cmd (str): The command to send to the device.

        Returns:
            str: The command output from the device.
        """
        return self.connection.send_command(cmd)

    def disconnect(self):
        """Disconnect from the network device."""
        self.connection.disconnect()


def get_platform_driver(platform):
    """Accepts a Platform model instance.

    Uses the platform's 'network_driver' field (set via Nautobot admin or API)
    as the Netmiko device_type.
    Returns a driver factory, or None if not set.
    """
    device_type = getattr(platform, "network_driver", None)
    if not device_type:
        return None

    def driver_factory(host, credentials):
        wrapper = NetmikoDriverWrapper(device_type, host, credentials)
        return wrapper.connect()

    return type("DynamicDriver", (), {"connect": staticmethod(driver_factory)})
