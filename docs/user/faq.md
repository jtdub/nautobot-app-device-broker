# Frequently Asked Questions

## General Questions

### What is the Device Broker app?

The Device Broker app is a comprehensive Nautobot application that provides a unified, platform-agnostic interface for executing commands on network devices. It leverages Nautobot's device inventory, platform definitions, and secrets management to enable secure, automated device interactions across multi-vendor network environments.

### Which network platforms are supported?

The app supports any network device platform that has a corresponding Netmiko driver. Platform support is configured through Nautobot's platform `network_driver` field, which maps to Netmiko device types. Common supported platforms include:

- **Cisco**: IOS, IOS-XE, NXOS, ASA
- **Arista**: EOS
- **Juniper**: JunOS
- **HPE/Aruba**: ProCurve, ArubaOS
- **Fortinet**: FortiOS
- **Dell**: Force10, PowerConnect
- **Many others**: Any platform with a Netmiko driver can be supported

New platforms can be added by simply configuring the platform's `network_driver` field in Nautobot to match the corresponding Netmiko device type - no code changes are required.

### How do I add support for a new platform?

Adding support for a new platform is straightforward and requires no code modifications:

1. **Create Platform in Nautobot**: Navigate to DCIM → Platforms → Add and create a new platform
2. **Configure Network Driver**: Set the `network_driver` field to the exact Netmiko device type (e.g., "fortinet" for FortiGate devices)
3. **Assign to Devices**: Assign the platform to your device records in Nautobot
4. **Configure Credentials**: Ensure devices have secrets groups with appropriate authentication credentials
5. **Test**: The platform will be automatically supported by Device Broker

**Example**:
- Platform Name: "Fortinet FortiGate"  
- Platform Slug: "fortinet-fortigate"
- Network Driver: "fortinet"

The app will dynamically load the appropriate Netmiko driver based on the platform configuration.

### How does authentication work?

The app uses Nautobot's secrets groups feature for device authentication. Each device must have a secrets group assigned that contains the necessary credentials for device access:

- **Required Secrets**: `username` and `password` are the minimum required secrets
- **Secrets Group Assignment**: Devices must have secrets groups assigned either individually or through inheritance
- **Secure Storage**: All credentials are stored securely within Nautobot's secrets management system
- **No External Dependencies**: No external authentication systems are required

## Configuration Questions

### How do I add support for a new platform?

Adding support for a new platform is straightforward and requires no code modifications:

1. **Create Platform in Nautobot**: Navigate to DCIM → Platforms → Add and create a new platform
2. **Configure Network Driver**: Set the `network_driver` field to the exact Netmiko device type (e.g., "fortinet" for FortiGate devices)
3. **Assign to Devices**: Assign the platform to your device records in Nautobot
4. **Configure Credentials**: Ensure devices have secrets groups with appropriate authentication credentials
5. **Test**: The platform will be automatically supported by Device Broker

**Example**:
- Platform Name: "Fortinet FortiGate"  
- Platform Slug: "fortinet-fortigate"
- Network Driver: "fortinet"

The app will dynamically load the appropriate Netmiko driver based on the platform configuration.

### What credentials are required in the secrets group?

The secrets group should contain:
- `username`: Device login username
- `password`: Device login password
- Optionally: `secret` for enable passwords (depending on platform requirements)

### Can I use different connection libraries besides Netmiko?

Yes, the app is designed to be extensible. You can modify the `get_platform_driver` function in `utils.py` to support different connection libraries by implementing the required interface methods (`connect`, `send_command`, `disconnect`, etc.).

## Usage Questions

### Can I execute commands on devices without entering configuration mode?

Yes, configuration mode is optional. When disabled, the app will execute commands in operational/user exec mode. This is appropriate for show commands and non-configuration operations.

### How do I target multiple devices?

You can target multiple devices using several methods:
- **Specific Selection**: Choose individual devices from the device list
- **Platform Filtering**: Target all devices of a specific platform
- **Location Filtering**: Target all devices in a specific location
- **Combination**: Use multiple selection methods together

### What happens if a device connection fails?

If a device connection fails, the job will:
- Log the error for that specific device
- Continue processing other devices in the selection
- Include the error information in the job results
- Not interrupt the execution for other devices

### What types of commands can I execute?

The app supports two primary modes of command execution:

**Operational Commands (Default Mode)**:
- Read-only commands that don't modify device configuration
- Examples: `show version`, `show interfaces`, `show ip route`
- Safe for regular monitoring and diagnostic operations

**Configuration Commands (Configuration Mode Enabled)**:
- Commands that modify device configuration or settings
- Automatically enters configuration mode before executing commands
- Examples: Interface configuration, routing protocol changes, security settings
- Requires careful planning and testing before execution

### Can I execute multiple commands in a single job?

Yes, the app supports multi-line command input. Simply enter one command per line in the commands field. The app will execute commands sequentially on each target device and provide consolidated results showing the output from each command.

### How do I target devices for command execution?

The app provides three flexible device selection methods that can be used individually or in combination:

1. **Individual Device Selection**: Choose specific devices from dropdown lists
2. **Platform-Based Selection**: Target all devices of a specific platform type
3. **Location-Based Selection**: Target all devices in a specific location (site, building, rack)

The app automatically combines selections from all methods and eliminates duplicates, giving you precise control over which devices receive commands.

## Troubleshooting

### "No platform driver" error

This error occurs when:
- The device's platform is not mapped in the `PLATFORM_TO_NETMIKO` dictionary
- The platform slug doesn't match the expected mapping
- The device has no platform assigned

**Solution**: Ensure the device has a platform assigned and that platform is supported by the app.

### "No secrets group" error

This error occurs when:
- The device has no secrets group assigned
- The secrets group exists but contains no secrets

**Solution**: Assign a properly configured secrets group to the device with the required credentials.

### Connection timeout errors

Connection timeouts can occur due to:
- Network connectivity issues
- Incorrect IP addresses
- Firewall restrictions
- Device availability

**Solution**: Verify network connectivity, correct IP addresses, and ensure the device is reachable from the Nautobot server.

### Authentication failures

Authentication failures typically result from:
- Incorrect credentials in the secrets group
- Account lockouts on the target device
- Privilege level restrictions

**Solution**: Verify credentials are correct and the account has appropriate privileges for the intended operations.

## Performance Questions

### How many devices can I target simultaneously?

The number of devices you can target depends on:
- Available system resources
- Network latency to target devices
- Device response times
- Job timeout configurations

For large device counts, consider breaking operations into smaller batches or running jobs during maintenance windows.

### Can I schedule Device Broker jobs?

Yes, you can schedule Device Broker jobs using Nautobot's built-in job scheduling capabilities. This is useful for regular maintenance tasks, monitoring, or compliance checking.

## Development Questions

### How can I extend the app's functionality?

The app can be extended by:
- Adding new platform drivers in `utils.py`
- Creating custom job variations for specific use cases
- Implementing additional error handling or logging
- Adding support for different connection libraries

### Can I integrate Device Broker with other automation tools?

Yes, the app can be integrated with:
- Nautobot's REST API for programmatic job execution
- External automation platforms via API calls
- CI/CD pipelines for infrastructure automation
- Custom scripts and applications
