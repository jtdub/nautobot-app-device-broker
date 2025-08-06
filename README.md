# Device Broker

<p align="center">
  <img src="https://raw.githubusercontent.com/jtdub/nautobot-app-device-broker/main/docs/images/icon-device-broker.png" class="logo" height="200px">
  <br>
  <a href="https://github.com/jtdub/nautobot-app-device-broker/actions"><img src="https://github.com/jtdub/nautobot-app-device-broker/actions/workflows/ci.yml/badge.svg?branch=main"></a>
  <a href="https://docs.nautobot.com/projects/device-broker/en/latest/"><img src="https://readthedocs.org/projects/nautobot-app-device-broker/badge/"></a>
  <a href="https://pypi.org/project/device-broker/"><img src="https://img.shields.io/pypi/v/device-broker"></a>
  <a href="https://pypi.org/project/device-broker/"><img src="https://img.shields.io/pypi/dm/device-broker"></a>
  <br>
  An <a href="https://networktocode.com/nautobot-apps/">App</a> for <a href="https://nautobot.com/">Nautobot</a>.
</p>

## Overview

The Device Broker app is a comprehensive platform-agnostic solution for executing commands on network devices directly from Nautobot. It provides a unified interface for interacting with diverse network equipment regardless of vendor or platform, eliminating the need for network operators to manage separate tools or scripts for device interaction.

Built on the powerful Netmiko library, Device Broker leverages Nautobot's existing device inventory, platform definitions, and secrets management to enable network operators to execute commands on single or multiple devices without needing to manage separate connection libraries or authentication mechanisms. The app supports both operational commands and configuration changes, making it a powerful tool for network automation workflows, troubleshooting, and bulk configuration management.

### Key Features

- **Universal Platform Support**: Supports any network device platform with a Netmiko driver through dynamic runtime configuration - no code changes required
- **Multi-device Operations**: Execute commands across multiple devices simultaneously with intelligent device selection and filtering
- **Flexible Targeting**: Select devices individually, by platform type, by location, or through combinations with automatic deduplication
- **Seamless Authentication**: Complete integration with Nautobot's secrets groups for secure credential management
- **Dual Operation Modes**: Support for both operational (read-only) and configuration commands with automatic mode switching
- **Comprehensive Logging**: Detailed per-device logging with complete audit trails and error reporting
- **Zero-Maintenance Platform Support**: Add new platform support through Nautobot configuration without app updates
- **API Integration**: Full programmatic access through Nautobot's job execution APIs

### Supported Platforms

Device Broker supports any platform with a corresponding Netmiko driver, including:
- **Cisco**: IOS, IOS-XE, NXOS, ASA
- **Arista**: EOS  
- **Juniper**: JunOS
- **HPE/Aruba**: ProCurve, ArubaOS
- **Fortinet**: FortiOS
- **Dell**: Force10, PowerConnect
- **Many others**: Expandable to any Netmiko-supported platform

### Screenshots

The Device Broker app provides an intuitive interface through Nautobot's job system for comprehensive network device command execution. The primary interface features:

**Core Interface Elements:**
- **Device Selection**: Multiple targeting methods including individual selection, platform filtering, location-based grouping, and combination targeting with automatic deduplication
- **Command Input**: Multi-line command input supporting complex sequences and operational workflows  
- **Execution Options**: Configuration mode toggle for operational vs. configuration commands with automatic mode switching
- **Progress Monitoring**: Real-time job execution progress with detailed per-device status and error tracking
- **Result Display**: Comprehensive output showing command results, errors, execution details, and complete audit trails

**Key Capabilities Demonstrated:**
- Unified command execution across multi-vendor environments without vendor-specific tools
- Flexible device targeting for precise operational control with intelligent filtering
- Secure credential handling through Nautobot's built-in secrets management with no hardcoded credentials
- Detailed audit trails for compliance and troubleshooting with comprehensive logging
- Scalable execution supporting both individual devices and large device populations with robust error handling
- Zero-maintenance platform support through dynamic configuration

The interface eliminates the complexity of managing multiple vendor-specific tools while providing enterprise-grade logging, error handling, and result management.

More detailed screenshots and usage examples can be found in the [Using the App](https://docs.nautobot.com/projects/device-broker/en/latest/user/app_use_cases/) section of the documentation.

## Documentation

Complete documentation for the Device Broker app is available through the Nautobot documentation system:

- **[User Guide](https://docs.nautobot.com/projects/device-broker/en/latest/user/app_overview/)** - App overview, getting started, and comprehensive usage patterns
- **[Administrator Guide](https://docs.nautobot.com/projects/device-broker/en/latest/admin/install/)** - Installation, configuration, and maintenance procedures
- **[Developer Guide](https://docs.nautobot.com/projects/device-broker/en/latest/dev/contributing/)** - Extending functionality, code reference, and contribution guidelines
- **[Release Notes](https://docs.nautobot.com/projects/device-broker/en/latest/admin/release_notes/)** - Version history, changelog, and migration guides
- **[FAQ](https://docs.nautobot.com/projects/device-broker/en/latest/user/faq/)** - Frequently asked questions and troubleshooting guidance

### Contributing to the Documentation

You can find all the Markdown source for the App documentation under the [`docs`](https://github.com/jtdub/nautobot-app-device-broker/tree/develop/docs) folder in this repository. For simple edits, a Markdown capable editor is sufficient: clone the repository and edit away.

If you need to view the fully-generated documentation site, you can build it with [MkDocs](https://www.mkdocs.org/). A container hosting the documentation can be started using the `invoke` commands (details in the [Development Environment Guide](https://docs.nautobot.com/projects/device-broker/en/latest/dev/dev_environment/#docker-development-environment)) on [http://localhost:8001](http://localhost:8001). Using this container, as your changes to the documentation are saved, they will be automatically rebuilt and any pages currently being viewed will be reloaded in your browser.

Any PRs with fixes or improvements are very welcome!

## Questions

For any questions or comments, please check the [FAQ](https://docs.nautobot.com/projects/device-broker/en/latest/user/faq/) first. Feel free to also swing by the [Network to Code Slack](https://networktocode.slack.com/) (channel `#nautobot`), sign up [here](http://slack.networktocode.com/) if you don't have an account.
