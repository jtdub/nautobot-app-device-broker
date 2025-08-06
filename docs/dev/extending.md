# Extending the App

The Device Broker app is designed to be extensible and can be enhanced in several ways to meet specific organizational needs or to add support for additional network platforms and features.

## Adding Support for New Platforms

The Device Broker app supports any platform with a corresponding Netmiko driver through dynamic platform mapping. **No code changes are required** to add new platforms - platform support is configured entirely through Nautobot's platform configuration.

### Step 1: Create Platform in Nautobot

Create a new platform in Nautobot through the admin interface or API:

1. **Navigate to**: DCIM → Platforms → Add
2. **Configure the following fields**:
    - **Name**: Display name for the platform (e.g., "Fortinet FortiGate")
    - **Slug**: Unique identifier for the platform (e.g., "fortinet-fortigate")
    - **Network Driver**: **Critical** - Set this to the exact Netmiko device type (e.g., "fortinet")

### Step 2: Verify Netmiko Support

Ensure that Netmiko supports your target platform. Check the [Netmiko documentation](https://github.com/ktbyers/netmiko) for a complete list of supported device types. The `network_driver` field must match exactly with a supported Netmiko device type.

Common Netmiko device types include:
- `cisco_ios` - Cisco IOS/IOS-XE devices
- `arista_eos` - Arista EOS devices
- `juniper_junos` - Juniper JunOS devices
- `fortinet` - Fortinet FortiGate devices
- `hp_procurve` - HPE ProCurve switches
- `aruba_os` - Aruba wireless controllers

### Step 3: Configure Device Records

Assign the new platform to your device records in Nautobot and ensure each device has:
- **Platform**: Set to your newly created platform
- **Primary IP Address**: Configured for SSH connectivity
- **Secrets Group**: Assigned with appropriate credentials containing at least:
    - `username` - SSH username
    - `password` - SSH password

### Step 4: Test the Implementation

Test your new platform support with a small number of devices before deploying to production. The Device Broker Job will automatically detect and use the platform's network driver configuration.

## Custom Driver Implementation

For platforms not supported by Netmiko or when you need custom connection logic, you can implement custom drivers.

### Creating a Custom Driver

1. **Implement the Driver Interface**: Create a class that implements the same interface as `NetmikoDriverWrapper`:

```python
class CustomDriverWrapper:
    """Custom driver for specialized network devices."""
    
    def __init__(self, device_type, host, credentials):
        self.device_type = device_type
        self.host = host
        self.credentials = credentials
        self.connection = None
    
    def connect(self):
        """Establish connection to the device."""
        # Implement your connection logic
        return self
    
    def enter_config_mode(self):
        """Enter configuration mode."""
        # Implement config mode logic
        pass
    
    def send_command(self, cmd):
        """Send command and return output."""
        # Implement command execution
        return "command output"
    
    def disconnect(self):
        """Disconnect from the device."""
        # Implement disconnection logic
        pass
```

2. **Update the Driver Factory**: Modify the `get_platform_driver` function to return your custom driver for specific platforms:

```python
def get_platform_driver(platform):
    """Get the appropriate driver for a given platform instance.
    
    Args:
        platform: Platform model instance with network_driver attribute
        
    Returns:
        Driver class with connect method, or None if no driver available
    """
    # Get the network_driver field from the platform object
    device_type = getattr(platform, 'network_driver', None)
    
    if not device_type:
        return None
    
    if device_type == "custom":
        def driver_factory(host, credentials):
            wrapper = CustomDriverWrapper(device_type, host, credentials)
            return wrapper.connect()
        return type("CustomDriver", (), {"connect": staticmethod(driver_factory)})
    
    # Default Netmiko implementation for all other device types
    def driver_factory(host, credentials):
        wrapper = NetmikoDriverWrapper(device_type, host, credentials)
        return wrapper.connect()
    
    return type("DynamicDriver", (), {"connect": staticmethod(driver_factory)})
```

## Extending Job Functionality

You can create custom job classes that extend or modify the base `DeviceBrokerJob` functionality.

### Creating Custom Jobs

```python
from device_broker.jobs import DeviceBrokerJob

class CustomDeviceBrokerJob(DeviceBrokerJob):
    """Custom job with additional functionality."""
    
    class Meta:
        name = "Custom Device Broker Job"
        description = "Extended device broker with custom features."
    
    # Add custom variables
    custom_option = BooleanVar(
        required=False,
        label="Custom Option",
        description="Enable custom processing"
    )
    
    def run(self, custom_option=False, **kwargs):
        """Override run method with custom logic."""
        if custom_option:
            self.logger.info("Custom option enabled")
            # Implement custom logic
        
        # Call parent implementation
        return super().run(**kwargs)
    
    def _process_device(self, device, commands_list, config_mode):
        """Override device processing with custom logic."""
        # Add custom pre-processing
        result = super()._process_device(device, commands_list, config_mode)
        # Add custom post-processing
        return result
```

### Registering Custom Jobs

```python
from nautobot.apps.jobs import register_jobs

register_jobs(CustomDeviceBrokerJob)
```

## Adding Configuration Options

Extend the app configuration to support additional settings.

### App Configuration Extension

```python
# In device_broker/__init__.py
class DeviceBrokerConfig(NautobotAppConfig):
    # ... existing configuration
    
    default_settings = {
        "custom_timeout": 30,
        "max_concurrent_connections": 10,
        "custom_feature_enabled": False,
    }
    
    required_settings = [
        # Add any required settings
    ]
```

### Using Configuration Settings

```python
from django.conf import settings

# Access app settings
app_settings = settings.PLUGINS_CONFIG.get("device_broker", {})
timeout = app_settings.get("custom_timeout", 30)
```

## Error Handling Extensions

Enhance error handling for specific use cases or platforms.

### Custom Exception Classes

```python
class DeviceBrokerError(Exception):
    """Base exception for Device Broker operations."""
    pass

class PlatformNotSupportedError(DeviceBrokerError):
    """Raised when a platform is not supported."""
    pass

class DeviceConnectionError(DeviceBrokerError):
    """Raised when device connection fails."""
    pass
```

### Enhanced Error Processing

```python
def _process_device_with_enhanced_errors(self, device, commands_list, config_mode):
    """Process device with enhanced error handling."""
    try:
        return self._process_device(device, commands_list, config_mode)
    except ConnectionError as exc:
        raise DeviceConnectionError(f"Failed to connect to {device.display}: {exc}")
    except Exception as exc:
        self.logger.error("Unexpected error processing %s: %s", device.display, exc)
        raise DeviceBrokerError(f"Processing failed for {device.display}: {exc}")
```

## Integration Extensions

### REST API Extensions

Add custom API endpoints for specialized functionality:

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def custom_device_operation(request):
    """Custom API endpoint for device operations."""
    # Implement custom logic
    return Response({"status": "success"})
```

### Database Model Extensions

If you need to store additional data related to device operations:

```python
from django.db import models
from nautobot.dcim.models import Device

class DeviceCommandHistory(models.Model):
    """Track command execution history."""
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    command = models.TextField()
    output = models.TextField()
    executed_at = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField()
```

## Testing Extensions

When extending the app, ensure you add appropriate tests:

### Unit Tests for Custom Drivers

```python
import unittest
from unittest.mock import Mock, patch
from device_broker.utils import get_platform_driver

class TestCustomDriver(unittest.TestCase):
    """Test custom driver functionality."""
    
    def test_custom_platform_driver(self):
        """Test that custom platform returns expected driver."""
        driver = get_platform_driver("custom_platform")
        self.assertIsNotNone(driver)
    
    @patch('device_broker.utils.CustomDriverWrapper')
    def test_driver_connection(self, mock_wrapper):
        """Test driver connection logic."""
        # Implement test logic
        pass
```

### Integration Tests

```python
from nautobot.apps.testing import TransactionTestCase
from device_broker.jobs import DeviceBrokerJob

class TestDeviceBrokerIntegration(TransactionTestCase):
    """Integration tests for Device Broker functionality."""
    
    def test_job_execution(self):
        """Test complete job execution workflow."""
        # Set up test data
        # Execute job
        # Verify results
        pass
```

## Contributing Extensions

When extending the app for community benefit:

1. **Open an Issue**: Discuss your planned extension before implementation
2. **Follow Coding Standards**: Maintain consistency with existing code style
3. **Add Documentation**: Document new features and configuration options
4. **Include Tests**: Ensure adequate test coverage for new functionality
5. **Update Examples**: Provide usage examples for new features

Extending the application is welcome, however it is best to open an issue first, to ensure that a PR would be accepted and makes sense in terms of features and design.
