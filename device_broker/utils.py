"""Device Broker utilities for network device platform drivers and connections."""

from __future__ import annotations

from typing import Optional

from napalm import get_network_driver as get_napalm_driver
from nautobot.dcim.models import Device
from netmiko import ConnectHandler


def get_group_credentials(device: Device) -> dict[str, str]:
    """Resolve secrets for a device from its SecretsGroup.

    Returns a mapping of secret_type -> secret value, preferring CLI-like access types.
    """
    creds: dict[str, str] = {}
    group = getattr(device, "secrets_group", None)
    if not group:
        return creds

    assocs = list(group.secrets_group_associations.all())
    if not assocs:
        return creds

    preferred = ("ssh", "network", "cli", "https", "http")
    access_types = {a.access_type for a in assocs}
    chosen_access_type = next((a for a in preferred if a in access_types), None) or next(iter(access_types))

    secret_types = [a.secret_type for a in assocs if a.access_type == chosen_access_type]

    for secret_type in secret_types:
        value: str | None = group.get_secret_value(
            access_type=chosen_access_type,
            secret_type=secret_type,
            obj=device,
        )
        if value:
            creds[secret_type] = value

    return creds


class NetmikoDriverWrapper:
    """Wrapper class for Netmiko connection handling with device platforms."""

    def __init__(self, device_type, host, credentials, timeout: Optional[int] = None):
        """Initialize the NetmikoDriverWrapper with connection parameters.

        Args:
            device_type (str): The Netmiko device type identifier.
            host (str): The host IP address or hostname.
            credentials (dict): Dictionary containing username and password.
            timeout (int | None): TCP connection timeout in seconds.
        """
        self.device_type = device_type
        self.host = host
        self.credentials = credentials
        self.timeout = timeout
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
        if self.timeout is not None:
            params["timeout"] = self.timeout
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


class NapalmDriverWrapper:
    """Wrapper for NAPALM connection handling and command execution."""

    def __init__(self, napalm_driver_name: str, host: str, credentials: dict, timeout: Optional[int] = None):
        """Initialize the NAPALM driver wrapper.

        Args:
            napalm_driver_name: The NAPALM driver name (e.g., "ios", "eos").
            host: Target hostname or IP address.
            credentials: Mapping with "username" and "password".
            timeout: TCP connection timeout in seconds.
        """
        self.napalm_driver_name = napalm_driver_name
        self.host = host
        self.credentials = credentials
        self.timeout = timeout
        self.connection = None

    def connect(self):
        """Open a NAPALM connection using the requested driver."""
        driver_cls = get_napalm_driver(self.napalm_driver_name)
        optional_args = {}
        if self.timeout is not None:
            optional_args["timeout"] = self.timeout
        self.connection = driver_cls(
            hostname=self.host,
            username=self.credentials.get("username"),
            password=self.credentials.get("password"),
            optional_args=optional_args or None,
        )
        self.connection.open()
        return self

    def enter_config_mode(self):
        """Best-effort config-mode. Many NAPALM drivers abstract this; noop by default."""
        return None

    def send_command(self, cmd: str) -> str:
        """Execute a raw command via the driver's CLI method if available.

        Args:
            cmd: The command to execute.

        Returns:
            The command output.

        Raises:
            NotImplementedError: If the underlying driver doesn't support CLI execution.
        """
        if hasattr(self.connection, "cli"):
            return self.connection.cli([cmd]).get(cmd, "")
        raise NotImplementedError("send_command is not supported by this NAPALM driver")

    def disconnect(self):
        """Close the NAPALM connection."""
        self.connection.close()


def get_platform_driver(platform, method: str = "netmiko"):
    """Return a driver factory object for the given platform and method.

    Args:
        platform: Nautobot Platform instance (expects `network_driver` attribute).
        method: Connection method, either "netmiko" or "napalm".

    Returns:
        A lightweight object exposing a static `connect(host, credentials, timeout)` method, or None.
    """
    device_type = getattr(platform, "network_driver", None)
    if not device_type:
        return None

    method_normalized = (method or "netmiko").lower()

    def driver_factory(host, credentials, timeout: Optional[int] = None):
        if method_normalized == "napalm":
            wrapper = NapalmDriverWrapper(device_type, host, credentials, timeout=timeout)
        else:
            wrapper = NetmikoDriverWrapper(device_type, host, credentials, timeout=timeout)
        return wrapper.connect()

    return type("DynamicDriver", (), {"connect": staticmethod(driver_factory)})
