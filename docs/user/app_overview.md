# App Overview

**Authentication and Security:**
The Device Broker app integrates seamlessly with Nautobot's secrets management system for secure credential handling:

- **Secrets Group Integration**: Device credentials are managed through Nautobot's secrets groups, eliminating the need for hardcoded credentials
- **Credential Isolation**: Each device can have different credentials through individual secrets group assignments
- **Secure Storage**: All authentication data is encrypted and managed through Nautobot's built-in security mechanisms
- **Audit Trail**: All device interactions are logged with complete credential usage trackinghis document provides an overview of the App including critical information and important considerations when applying it to your Nautobot environment.

!!! note
    Throughout this documentation, the terms "app" and "plugin" will be used interchangeably.

## Description

The Device Broker app is a comprehensive network automation tool that enables direct command execution on network devices from within Nautobot. Designed as a platform-agnostic solution, it provides a unified interface for interacting with diverse network equipment regardless of vendor or platform, eliminating the need for network operators to manage separate tools or scripts for device interaction.

**Core Capabilities:**

- **Universal Device Support**: Leverages Netmiko's extensive platform support, automatically mapping Nautobot platform definitions to appropriate network drivers
- **Multi-device Operations**: Execute identical commands across multiple devices simultaneously, perfect for bulk operations and consistency checks
- **Flexible Device Targeting**: Select devices through multiple methods including individual selection, platform-based filtering, or location-based grouping
- **Secure Authentication**: Integrates seamlessly with Nautobot's secrets groups, eliminating the need to manage credentials separately
- **Dual Operation Modes**: Supports both operational commands (show commands, status checks) and configuration changes with automatic mode switching
- **Comprehensive Audit Trail**: Provides detailed logging of all device interactions, command execution, and results for compliance and troubleshooting

**Primary Use Cases:**

- **Network Troubleshooting**: Quickly gather diagnostic information from multiple devices during outages or performance issues
- **Bulk Configuration Management**: Deploy consistent configuration changes across device groups, locations, or entire networks
- **Compliance Auditing**: Regularly collect configuration and status information for security and compliance reporting
- **Network Monitoring**: Execute custom monitoring commands and collect real-time data from network devices
- **Change Validation**: Verify configuration changes and system status after maintenance activities
- **Automation Integration**: Serve as a foundation for larger network automation workflows and custom scripts

The app is particularly valuable for organizations managing multi-vendor environments, large-scale networks, or teams implementing Infrastructure as Code (IaC) practices where consistent, repeatable device interactions are essential.


## Audience (User Personas) - Who should use this App?

The Device Broker app is designed for:

- **Network Engineers**: Professionals who need to execute commands across multiple network devices for troubleshooting, monitoring, or configuration management
- **Network Operations Teams**: Teams responsible for day-to-day network operations who require quick access to device information and configuration changes
- **DevOps/NetOps Engineers**: Engineers implementing network automation workflows who need a reliable interface for device interaction
- **System Integrators**: Professionals working with multi-vendor network environments who need a unified approach to device management
- **Network Administrators**: Administrators managing large network infrastructures who need efficient tools for bulk operations

The app is particularly valuable for organizations with:
- Multi-vendor network environments
- Large-scale network infrastructures requiring bulk operations
- Teams implementing Infrastructure as Code (IaC) practices
- Organizations seeking to standardize network device interactions through Nautobot

## Authors and Maintainers

- **James Williams** ([@jtdub](https://github.com/jtdub)) - Primary Author and Maintainer

## Nautobot Features Used

The Device Broker app integrates with several core Nautobot features:

### Core Models

The Device Broker app integrates deeply with Nautobot's core data models:

- **Devices**: The foundation of all operations, the app queries Nautobot's device inventory to determine target devices for command execution
- **Platforms**: Critical for driver selection, the app uses each device's platform assignment and its `network_driver` field to determine the appropriate Netmiko driver
- **Locations**: Enables location-based device filtering, allowing operators to target entire sites, buildings, or racks with a single job execution
- **Secrets Groups**: Essential for authentication, devices must have assigned secrets groups containing the necessary credentials (username, password) for SSH access
- **Primary IP Addresses**: Used as the connection target for device SSH sessions

### Jobs Framework

The app implements a single, comprehensive job class:

- **Device Broker Job**: The primary interface for all device command execution, featuring:
    - Multi-method device selection (individual, platform-based, location-based)
    - Multi-line command input supporting complex command sequences
    - Configuration mode toggle for operational vs. configuration commands
    - Comprehensive result aggregation and error handling
    - Real-time progress logging and detailed per-device output

### API Integration

While the app doesn't expose custom API endpoints, it leverages Nautobot's existing APIs:

- **Device Management APIs**: Retrieves device information, platform details, and IP addresses
- **Secrets Management APIs**: Accesses credential information from assigned secrets groups
- **Jobs API**: Can be triggered programmatically through Nautobot's job execution endpoints

### User Interface

The app provides documentation access through Nautobot's interface:

- **Static Documentation**: Comprehensive documentation served through Nautobot's static file handling
- **Job Execution Interface**: Full integration with Nautobot's job management system for user-friendly command execution

### Extras

#### Jobs

- **Device Broker Job**: The comprehensive job for executing commands on network devices with these capabilities:
    - **Device Selection Methods**: 
        - Individual device selection from dropdown lists
        - Platform-based filtering to target all devices of a specific platform type
        - Location-based filtering to target devices by site, building, or rack
        - Combination filtering for precise device targeting
    - **Command Execution Features**:
        - Multi-line command input supporting complex command sequences
        - Configuration mode toggle (enabled/disabled) for operational vs. configuration commands
        - Per-device credential retrieval from assigned secrets groups
        - Dynamic driver selection based on platform definitions
    - **Results and Logging**:
        - Comprehensive per-device result logging with command output
        - Detailed error handling and reporting for connection failures
        - Job-level aggregation of all device results
        - Real-time progress tracking and status updates

#### Configuration

The app utilizes Nautobot's platform management for driver configuration:

- **Platform Network Driver Field**: Each platform's `network_driver` field maps to the corresponding Netmiko device type
- **No Custom Configuration Required**: The app automatically adapts to any platform with a defined network driver
- **Dynamic Driver Loading**: Platform-to-driver mapping is handled dynamically at runtime based on device platform assignments
