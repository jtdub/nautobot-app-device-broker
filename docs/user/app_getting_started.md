# Getting Started with the App

This document provides a step-by-step tutorial on how to get the App going and how to use it.

## Install the App

To install the App, please follow the instructions detailed in the [Installation Guide](../admin/install.md).

## First steps with the App

Once the Device Broker app is installed and configured, you can begin using it to execute commands on your network devices. Here's how to get started:

### Prerequisites

Before using the Device Broker app, ensure your environment meets these requirements:

**1. Device Configuration in Nautobot:**

- **Device Records**: Network devices must be properly defined in Nautobot's device inventory
- **Platform Assignment**: Each device must have a platform assigned with a configured `network_driver` field
- **Primary IP Address**: Devices must have primary IP addresses configured for SSH connectivity
- **Secrets Group Assignment**: Each device must have a secrets group assigned containing authentication credentials

**2. Supported Network Platforms:**

The app supports any platform with a Netmiko driver. Common examples include:

- **Cisco IOS/IOS-XE**: `cisco_ios` driver
- **Arista EOS**: `arista_eos` driver  
- **Juniper JunOS**: `juniper_junos` driver
- **Cisco NXOS**: `cisco_nxos` driver
- **HPE/Aruba**: `hp_procurve` or `aruba_os` drivers
- **Many others**: Any Netmiko-supported platform can be used

**3. Network Connectivity:**

- **SSH Access**: Nautobot server must have SSH connectivity to target devices
- **Port Access**: TCP port 22 (or custom SSH ports) must be accessible
- **Firewall Rules**: Appropriate firewall rules allowing SSH from Nautobot to devices

**4. Authentication Configuration:**

- **Secrets Groups**: Create secrets groups in Nautobot containing device credentials
- **Required Secrets**: Each secrets group must contain:
    - `username`: Device login username
    - `password`: Device login password
- **Device Assignment**: Assign appropriate secrets groups to devices or device groups

**5. Platform Driver Configuration:**

- **Network Driver Field**: Set the `network_driver` field for each platform to the corresponding Netmiko device type
- **Example Mappings**:
    - Cisco IOS platform → `network_driver` = `cisco_ios`
    - Arista EOS platform → `network_driver` = `arista_eos`
    - Juniper JunOS platform → `network_driver` = `juniper_junos`

### Running Your First Device Command

**Step 1: Access the Job**
1. Navigate to **Jobs** in the Nautobot interface
2. Locate and select "Device Broker Job" from the available jobs list
3. Click to open the job execution form

**Step 2: Select Target Devices**
Choose your target devices using one or more of these methods:

- **Individual Device Selection**: 
    - Use the "Devices" dropdown to select specific devices
    - Hold Ctrl/Cmd to select multiple individual devices

- **Platform-Based Selection**: 
    - Use the "Platform" dropdown to target all devices of a specific platform
    - Useful for platform-wide operations or updates

- **Location-Based Selection**: 
    - Use the "Location" dropdown to target all devices in a specific location
    - Ideal for site-wide maintenance or troubleshooting

- **Combined Selection**: 
    - Use multiple selection methods simultaneously
    - The app will combine all selections and deduplicate devices automatically

**Step 3: Configure Command Execution**

- **Commands Field**: Enter the commands you want to execute
    - One command per line for multiple commands
    - Support for complex command sequences
    - Standard CLI commands as you would type on the device console

- **Configuration Mode**: Toggle this option based on your needs:
    - **Disabled** (default): For operational commands (show commands, status checks)
    - **Enabled**: For configuration commands that modify device settings

**Step 4: Execute the Job**
1. Review your selections and command input
2. Click "Run Job" to begin execution
3. Monitor the job progress in real-time
4. Review detailed results once execution completes

**Step 5: Analyze Results**
The job output provides:
- **Per-device results**: Individual output for each target device
- **Command execution status**: Success/failure status for each device
- **Error reporting**: Detailed error messages for any failures
- **Execution logs**: Complete audit trail of all operations

### Example Use Cases

- **Information Gathering**: Execute `show version` across multiple devices to collect firmware information
- **Configuration Backup**: Run `show running-config` to backup device configurations
- **Interface Status Check**: Use `show ip interface brief` to check interface status across multiple devices
- **Configuration Changes**: Enable configuration mode and push configuration commands

## What are the next steps?

After successfully executing your first commands with Device Broker, consider these next steps:

### Advanced Usage Patterns

**Bulk Configuration Management**
- Use platform or location filtering to deploy consistent configurations across device groups
- Leverage configuration mode for making systematic changes to network infrastructure
- Implement standardized configuration templates across multi-vendor environments

**Network Auditing and Compliance**
- Create scheduled jobs to regularly collect compliance information from devices
- Use operational commands to gather configuration data for security audits
- Monitor configuration drift by comparing device states over time

**Troubleshooting Workflows**
- Develop standardized troubleshooting command sets for different network scenarios
- Use location-based filtering to quickly diagnose site-wide issues
- Combine multiple diagnostic commands in sequence for comprehensive problem analysis

**Monitoring and Data Collection**
- Execute custom monitoring commands to supplement traditional SNMP monitoring
- Collect real-time performance data from devices during peak usage periods
- Gather detailed interface statistics and environmental data for capacity planning

### Integration Opportunities

**Automation Workflows**
- Integrate Device Broker jobs into larger automation workflows using Nautobot's API
- Trigger device command execution from external automation platforms
- Use job results as input for subsequent automation steps

**API Integration**
- Programmatically execute Device Broker jobs through Nautobot's REST API
- Parse job results for integration with external monitoring and management systems
- Automate job scheduling for regular maintenance and monitoring tasks

**Change Management Integration**
- Incorporate device command execution into formal change management processes
- Use pre-change and post-change command execution for verification and rollback
- Document device interactions as part of change audit trails

### Platform Extension and Customization

**Adding New Platform Support**
- Extend platform support by configuring the `network_driver` field for new platform types
- Any Netmiko-supported platform can be added without code changes
- Test new platform drivers in isolated environments before production deployment

**Custom Error Handling**
- Leverage job logging for custom error handling and alerting integrations
- Implement retry mechanisms for transient connection failures
- Create custom notification workflows based on job results

**Enhanced Automation**
- Build custom jobs that extend Device Broker functionality for specific use cases
- Integrate with other Nautobot apps for comprehensive network automation workflows
- Develop custom reporting and analytics based on command execution results

You can check out the [Use Cases](app_use_cases.md) section for more detailed examples and advanced usage patterns.
