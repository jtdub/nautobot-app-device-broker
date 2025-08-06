# Device Broker Code Reference

The Device Broker app consists of several key modules that provide platform-agnostic network device command execution capabilities through dynamic platform driver mapping.

## Core Modules

### device_broker.jobs
Contains the primary job class for device command execution with advanced device selection and filtering capabilities.

::: device_broker.jobs
    options:
        show_submodules: True

### device_broker.utils  
Contains utility functions for dynamic platform driver management and Netmiko connection handling.

::: device_broker.utils
    options:
        show_submodules: True

## Module Overview

The app architecture follows a simple but effective design with dynamic platform support:

- **Jobs Module**: Implements the DeviceBrokerJob class that handles:
    - Multi-method device selection (individual, platform-based, location-based)  
    - Device filtering and deduplication logic
    - Secrets group credential resolution
    - Command execution orchestration with error handling
  
- **Utils Module**: Provides:
    - Dynamic platform driver abstraction using Nautobot's platform `network_driver` field
    - NetmikoDriverWrapper for consistent connection management
    - Runtime driver factory creation based on platform configuration
  
- **URL Configuration**: Defines app routing and documentation access points

## Key Implementation Details

### Dynamic Platform Support
The app supports any Netmiko-compatible platform through runtime configuration:
    - No hardcoded platform mappings
    - Platform support configured via Nautobot's platform `network_driver` field
    - Automatic driver resolution at job execution time

### Secrets Integration
Authentication is handled through Nautobot's built-in secrets management:
    - Device secrets groups provide username/password credentials
    - Runtime credential resolution from assigned secrets groups
    - Secure credential handling with no hardcoded authentication

### Device Selection Logic
Advanced device targeting with multiple selection methods:
    - Individual device selection from multi-select dropdown
    - Platform-based filtering for bulk operations
    - Location-based filtering for site-wide tasks
    - Automatic deduplication when combining selection methods

The modular design allows for easy extension and customization while maintaining a clean separation of concerns between user interface, business logic, and device communication.
