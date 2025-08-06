# Device Broker Package Reference

This page provides comprehensive documentation for all modules and classes in the Device Broker app.

::: device_broker
    options:
        show_submodules: True
        show_source: True
        members_order: alphabetical
        
## Package Structure

The Device Broker app is organized into the following key modules:

- **`__init__.py`**: App configuration and metadata
- **`jobs.py`**: Device Broker Job implementation
- **`utils.py`**: Platform driver utilities and connection management  
- **`urls.py`**: URL routing and documentation access

## Key Classes and Functions

### DeviceBrokerConfig
App configuration class that defines app metadata, version information, and Nautobot integration settings.

### DeviceBrokerJob  
The primary job class that handles device selection, command execution, and result aggregation across multiple network devices. Features include:

- **Multi-method Device Selection**: Individual devices, platform filtering, location filtering, and combinations
- **Secrets Group Integration**: Automatic credential resolution from Nautobot's secrets groups  
- **Dynamic Driver Loading**: Runtime platform driver resolution using Nautobot's platform configuration
- **Configuration Mode Support**: Automatic mode switching for operational vs configuration commands
- **Comprehensive Error Handling**: Per-device error handling with detailed logging and reporting

### NetmikoDriverWrapper
Utility class that provides a consistent interface for Netmiko connections across different network device platforms with:

- **Connection Management**: Automatic SSH connection establishment and cleanup
- **Command Execution**: Standardized command sending with output capture
- **Configuration Mode**: Automatic configuration mode entry when required
- **Error Handling**: Connection and command execution error management

### get_platform_driver
Function that dynamically maps Nautobot platform definitions to appropriate Netmiko device drivers:

- **Dynamic Resolution**: Uses platform's `network_driver` field for runtime driver selection
- **No Code Changes**: Platform support added through Nautobot configuration only
- **Driver Factory**: Returns connection factory for the specified platform
- **Fallback Handling**: Graceful handling of unsupported or misconfigured platforms
