"""Device Broker Jobs module for executing commands on network devices."""

from django.db.models import Q
from nautobot.apps.jobs import (
    BooleanVar,
    ChoiceVar,
    IntegerVar,
    Job,
    MultiObjectVar,
    ObjectVar,
    TextVar,
    register_jobs,
)
from nautobot.dcim.models import Device, Location, Platform

from device_broker.utils import get_group_credentials, get_platform_driver


class DeviceBrokerJob(Job):
    """Job for executing commands on network devices using platform-specific drivers."""

    class Meta:  # pylint: disable=too-few-public-methods
        """Job metadata configuration."""

        name = "Device Broker Job"
        description = "Execute commands on selected devices using platform drivers and secrets."

    devices = MultiObjectVar(Device, required=False, description="Select specific devices (optional).")
    platform = ObjectVar(Platform, required=False, description="Filter devices by platform (optional).")
    location = ObjectVar(Location, required=False, description="Filter devices by location (optional).")
    config_mode = BooleanVar(required=True, label="Enter configuration mode?", default=False)
    commands = TextVar(required=True, label="List of Commands", description="Enter one command per line.")
    connection_timeout = IntegerVar(
        required=False,
        default=30,
        label="Connection Timeout (seconds)",
        description="TCP connection timeout for device sessions.",
    )
    connection_method = ChoiceVar(
        choices=[("netmiko", "Netmiko"), ("napalm", "NAPALM")],
        default="netmiko",
        label="Connection Method",
        description="Choose the transport library used to connect to devices.",
    )

    def _get_devices(self, devices, platform, location):
        """Merge device lists from the selected sources, deduplicate."""
        queryset = Device.objects.all()
        filters = Q()
        if platform:
            filters |= Q(platform=platform)
        if location:
            filters |= Q(location=location)
        filtered_devices = queryset.filter(filters).distinct() if filters else Device.objects.none()
        all_devices = set(devices or []) | set(filtered_devices)
        return list(all_devices)

    def run(
        self,
        devices,
        platform,
        location,
        config_mode,
        commands,
        connection_timeout=30,
        connection_method="netmiko",
        **kwargs,
    ):  # pylint: disable=too-many-arguments,arguments-differ
        """Execute commands on selected devices using their platform drivers.

        Args:
            devices: List of specific devices to target
            platform: Platform filter for device selection
            location: Location filter for device selection
            config_mode: Whether to enter configuration mode
            commands: Commands to execute on devices
            connection_timeout (int): TCP connection timeout in seconds (default 30)
            connection_method (str): "netmiko" or "napalm" (default "netmiko")
            **kwargs: Additional keyword arguments

        Returns:
            str: Formatted results from all device command executions
        """
        results = []
        commands_list = [cmd.strip() for cmd in commands.strip().splitlines() if cmd.strip()]
        devices_to_run = self._get_devices(devices, platform, location)
        if not devices_to_run:
            self.logger.warning("No devices matched the provided filters.")
            return "No devices to execute against."

        for device in devices_to_run:
            result = self._process_device(
                device,
                commands_list,
                config_mode,
                connection_timeout=connection_timeout,
                connection_method=connection_method,
            )
            if result:
                results.append(result)

        return "\n\n".join(results)

    def _process_device(  # pylint: disable=too-many-arguments
        self,
        device,
        commands_list,
        config_mode,
        connection_timeout,
        connection_method,
    ):
        """Process a single device and execute commands.

        Args:
            device: Device object to process
            commands_list: List of commands to execute
            config_mode: Whether to enter configuration mode
            connection_timeout (int): TCP connection timeout in seconds
            connection_method (str): "netmiko" or "napalm"

        Returns:
            str or None: Result string if device processed, None if skipped
        """
        self.logger.info("Processing device: %s", device.display)
        if not device.platform:
            self.logger.error("Device %s has no platform defined. Skipping.", device.display)
            return f"{device.display}: No platform defined, skipped."

        if hasattr(device, "secrets_group") and device.secrets_group:
            creds = get_group_credentials(device)
        else:
            self.logger.error("Device %s has no secrets group. Skipping.", device.display)
            return f"{device.display}: No secrets group, skipped."

        driver = get_platform_driver(device.platform, method=connection_method)
        if driver is None:
            self.logger.error("No driver found for platform: %s. Skipping device %s.", device.platform, device.display)
            return f"{device.display}: No platform driver, skipped."

        try:
            connection = driver.connect(
                host=str(device.primary_ip.address.ip) if device.primary_ip else device.name,
                credentials=creds,
                timeout=connection_timeout,
            )
            if config_mode:
                connection.enter_config_mode()

            command_results = []
            for cmd in commands_list:
                output = connection.send_command(cmd)
                self.logger.info("Device %s Command '%s' Output:\n%s", device.display, cmd, output)
                command_results.append(f"Command: {cmd}\nOutput:\n{output}")
            connection.disconnect()
            return f"{device.display}:\n" + "\n".join(command_results)
        except Exception as exc:  # pylint: disable=broad-exception-caught
            self.logger.error("Exception processing device %s: %s", device.display, exc)
            return f"{device.display}: Error - {str(exc)}"


name = "Device Broker"  # pylint: disable=invalid-name
register_jobs(DeviceBrokerJob)
