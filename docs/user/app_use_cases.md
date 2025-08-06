# Using the App

This document provides comprehensive examples and practical scenarios for leveraging the Device Broker app's capabilities in real-world network operations, automation workflows, and management tasks.

## General Usage

The Device Broker app is accessed through Nautobot's Jobs interface, providing a streamlined way to execute commands on network devices across your infrastructure. The app's unified interface eliminates the complexity of managing multiple vendor-specific tools while leveraging Nautobot's existing device inventory and credential management.

### Primary Access Method

1. **Navigate to Jobs**: Access the Jobs section in Nautobot's main navigation
2. **Select Device Broker Job**: Choose the "Device Broker Job" from the available jobs list
3. **Configure Execution Parameters**: Set up device selection, commands, and execution options
4. **Execute and Monitor**: Run the job and monitor progress through Nautobot's job execution interface

### Core Workflow Pattern

The app follows a consistent workflow pattern regardless of the specific use case:

**Device Targeting** → **Command Definition** → **Execution Configuration** → **Job Execution** → **Result Analysis**

This standardized approach ensures consistent operation across different network platforms, device types, and operational scenarios.

## Use-cases and Common Workflows

### Network Troubleshooting and Diagnostics

**Scenario**: Investigating network connectivity issues affecting multiple sites

**Workflow**:
1. **Target Selection**: Use location-based filtering to select all devices at affected sites
2. **Diagnostic Commands**: Execute troubleshooting commands such as:
   ```
   show ip route
   show interface status
   show version
   ping 8.8.8.8
   ```
3. **Analysis**: Review per-device output to identify patterns and root causes
4. **Follow-up**: Execute additional targeted commands based on initial findings

**Benefits**: Rapid data collection across multiple devices, consistent diagnostic approach, comprehensive logging for later analysis

### Bulk Configuration Management

**Scenario**: Deploying standard security configurations across all edge routers

**Workflow**:
1. **Platform Targeting**: Select all devices with platform "cisco_ios" or specific router platforms
2. **Configuration Commands**: Enable configuration mode and execute:
   ```
   service password-encryption
   ip ssh version 2
   line vty 0 4
   transport input ssh
   ```
3. **Verification**: Execute show commands to verify configuration deployment
4. **Documentation**: Job results provide complete audit trail of changes

**Benefits**: Consistent configuration deployment, reduced manual errors, comprehensive change documentation

### Compliance Auditing and Monitoring

**Scenario**: Regular security compliance checks across the network infrastructure

**Workflow**:
1. **Comprehensive Targeting**: Select devices across multiple platforms and locations
2. **Compliance Commands**: Execute audit commands such as:
   ```
   show running-config | include username
   show ip ssh
   show ntp status
   show logging
   ```
3. **Scheduled Execution**: Set up regular job execution for ongoing compliance monitoring
4. **Trend Analysis**: Compare results over time to track compliance status

**Benefits**: Automated compliance checking, standardized audit procedures, historical compliance tracking

### Network Inventory and Asset Management

**Scenario**: Collecting detailed hardware and software inventory information

**Workflow**:
1. **Network-wide Selection**: Target all devices or specific device categories
2. **Inventory Commands**: Execute information gathering commands:
   ```
   show version
   show inventory
   show module
   show license
   ```
3. **Data Collection**: Gather comprehensive device information for asset tracking
4. **Integration**: Use results for CMDB updates and asset management processes

**Benefits**: Automated inventory collection, accurate asset tracking, software license management

### Performance Monitoring and Capacity Planning

**Scenario**: Collecting performance data during peak usage periods

**Workflow**:
1. **Critical Device Selection**: Target core network devices and high-traffic interfaces
2. **Performance Commands**: Execute monitoring commands:
   ```
   show interfaces
   show processes cpu
   show memory
   show environment
   ```
3. **Regular Execution**: Schedule jobs during different time periods for trend analysis
4. **Capacity Analysis**: Use data for network capacity planning and optimization

**Benefits**: Real-time performance data, proactive capacity management, historical performance trends

### Change Validation and Verification

**Scenario**: Verifying successful completion of maintenance activities

**Workflow**:
1. **Target Affected Devices**: Select devices involved in recent changes
2. **Pre-change Baseline**: Execute commands before changes for comparison:
   ```
   show ip route summary
   show interface summary
   show version
   ```
3. **Post-change Verification**: Execute same commands after changes
4. **Comparison Analysis**: Compare before/after results to validate changes

**Benefits**: Systematic change validation, rollback decision support, change impact assessment

### Emergency Response and Incident Management

**Scenario**: Rapid information gathering during network incidents

**Workflow**:
1. **Incident Scope Selection**: Quickly target devices in affected areas
2. **Emergency Diagnostics**: Execute critical diagnostic commands:
   ```
   show logging | last 100
   show interface status
   show ip route summary
   show processes cpu sorted
   ```
3. **Real-time Analysis**: Gather information for incident response teams
4. **Documentation**: Maintain detailed logs for post-incident review

**Benefits**: Rapid incident response, consistent diagnostic approach, comprehensive incident documentation

## Best Practices

### Device Selection Strategy

**Use Appropriate Granularity**: 
- Individual devices for specific troubleshooting
- Platform filtering for standardization across device types
- Location filtering for site-wide operations
- Combined filtering for precise targeting

**Test with Small Groups**: Always test command sequences on a small subset of devices before executing across large device populations

### Command Design and Safety

**Operational vs. Configuration Mode**:
- Use operational mode (default) for read-only commands and diagnostics
- Enable configuration mode only when making actual device changes
- Test configuration commands in lab environments before production use

**Command Sequencing**:
- Structure commands logically from general to specific information
- Include verification commands after configuration changes
- Use appropriate command spacing for complex sequences

### Error Handling and Recovery

**Monitor Job Execution**: Always monitor job progress and review results for any failures or unexpected output

**Connection Failure Handling**: 
- Investigate and resolve connectivity issues for failed devices
- Re-run jobs on failed devices after resolving connection problems
- Document any persistent connectivity issues for infrastructure team follow-up

**Result Validation**: Review command output for each device to ensure expected results and identify any anomalies

### Security and Compliance

**Credential Management**: Ensure secrets groups are properly configured and regularly audited for appropriate access controls

**Change Documentation**: Use job results as part of change management documentation and audit trails

**Access Control**: Limit job execution permissions to appropriate personnel based on operational responsibilities

### Scalability and Performance

**Batch Size Management**: For very large device populations, consider breaking operations into smaller batches to manage execution time and resource usage

**Timing Considerations**: Schedule resource-intensive jobs during maintenance windows or low-traffic periods

**Result Storage**: Regularly archive or purge old job results to maintain system performance and storage efficiency

## Screenshots

*Note: Screenshots showing the Device Broker Job interface, execution results, and various use case examples would be valuable additions to this documentation. Consider adding images that demonstrate:*

- *Device selection interface with different filtering options*
- *Command input and configuration mode settings*
- *Job execution progress and results display*
- *Examples of successful bulk operations across multiple devices*
- *Error handling and troubleshooting result examples*
- **Configuration Mode**: Disabled
- **Commands**:
  ```
  show log | tail 50
  show interface counters errors
  show spanning-tree
  show ip route summary
  ```

**Benefit**: Quickly collect diagnostic information from multiple devices to accelerate problem resolution.

### VLAN Management

**Use Case**: Verify VLAN configuration consistency across switches

**Configuration**:
- **Platform**: Select switch platform
- **Configuration Mode**: Disabled
- **Commands**:
  ```
  show vlan brief
  show spanning-tree summary
  show interfaces trunk
  ```

**Benefit**: Ensure VLAN configurations are consistent across your switched infrastructure.

## Best Practices

### Device Selection Strategy
- Use **specific device selection** for targeted operations
- Use **platform filtering** for platform-specific commands
- Use **location filtering** for site-based operations

### Command Organization
- Group related commands together in a single job execution
- Use descriptive job names when scheduling recurring operations
- Test commands on a single device before bulk execution

### Error Handling
- Monitor job logs for connection failures or command errors
- Ensure devices have proper secrets group configurations
- Verify platform mappings are correct for your device types

### Security Considerations
- Use configuration mode only when necessary
- Review configuration commands before execution
- Ensure proper access controls are in place for job executionApp

This document describes common use-cases and scenarios for this App.

## General Usage

## Use-cases and common workflows

## Screenshots

!!! warning "Developer Note - Remove Me!"
    Ideally captures every view exposed by the App. Should include a relevant dataset.
