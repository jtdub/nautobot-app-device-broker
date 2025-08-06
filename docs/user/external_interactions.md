# External Interactions

This document describes external dependencies, system requirements, and integration points for the Device Broker app.

## External System Dependencies

### Network Device Connectivity

The Device Broker app requires network connectivity and proper configuration for device access:

**Connection Requirements:**

- **SSH Access**: Devices must be accessible via SSH from the Nautobot server
- **Port Requirements**: TCP port 22 (SSH) or custom SSH ports as configured on devices
- **Network Routing**: Nautobot server must have IP connectivity to device management interfaces
- **Firewall Configuration**: Appropriate firewall rules must allow SSH connections from Nautobot to target devices

**IP Address Resolution:**
- Primary IP addresses from Nautobot device records are used as connection targets
- If no primary IP is configured, the device name is used as the connection target
- Ensure DNS resolution is available if using device names for connections

### Device Management Protocols

**Primary Protocol Support:**
- **SSH**: Primary protocol for all device connections via Netmiko library
- **Platform Flexibility**: Any SSH-capable device with Netmiko driver support

**Connection Library:**
- **Netmiko**: All device connections are handled through the Netmiko library
- **Driver Mapping**: Platform network_driver field maps directly to Netmiko device types
- **Connection Management**: Automatic connection establishment, command execution, and cleanup

### Authentication Systems

The app integrates with Nautobot's built-in authentication and secrets management:

**Primary Authentication Method:**
- **Nautobot Secrets Groups**: All device credentials are stored and managed through Nautobot's secrets system
- **Required Credentials**: Each secrets group must contain `username` and `password` secrets for device access
- **Secure Storage**: Credentials are encrypted and stored securely within Nautobot's database

**Device-Credential Association:**
- **Secrets Group Assignment**: Devices must have secrets groups assigned either individually or through inheritance
- **Automatic Retrieval**: The app automatically retrieves appropriate credentials from the device's assigned secrets group
- **Dynamic Resolution**: Credentials are resolved at runtime based on device configuration

**Required Secret Names:**
The Device Broker app expects specific secret names within the assigned secrets group:
- **`username`**: SSH username for device authentication
- **`password`**: SSH password for device authentication

**Authentication Workflow:**
1. Device Broker checks if the device has an assigned secrets group
2. Retrieves all secrets from the assigned group
3. Extracts username and password values for SSH authentication
4. Uses credentials for secure connection establishment via Netmiko

**Security Considerations:**
- **Access Control**: Nautobot's standard user permissions control access to device broker jobs
- **Credential Security**: All device credentials are handled securely through Nautobot's built-in secrets management
- **Audit Trail**: All device interactions are logged for security and compliance purposes

## External Libraries and Dependencies

### Netmiko

The app depends on the Netmiko library for device connections:

- **Purpose**: Provides SSH connectivity and command execution capabilities
- **Supported Platforms**: Extensive support for network device platforms
- **Version**: Specified in `pyproject.toml` (currently `^4.6.0`)

### Platform Driver Support

Device platform support is provided through Netmiko's platform drivers with dynamic configuration:

**Dynamic Platform Support:**
- **No Code Changes Required**: Platform support is configured through Nautobot's platform `network_driver` field
- **Netmiko Integration**: Any platform supported by Netmiko can be used by setting the appropriate driver name
- **Runtime Resolution**: Platform drivers are resolved dynamically at job execution time

**Common Platform Examples:**

| Platform Family | Example Network Driver | Configuration |
|----------------|----------------------|---------------|
| Cisco IOS/IOS-XE | `cisco_ios` | Set platform `network_driver` = `cisco_ios` |
| Arista EOS | `arista_eos` | Set platform `network_driver` = `arista_eos` |  
| Juniper JunOS | `juniper_junos` | Set platform `network_driver` = `juniper_junos` |
| Cisco NXOS | `cisco_nxos` | Set platform `network_driver` = `cisco_nxos` |
| Fortinet FortiGate | `fortinet` | Set platform `network_driver` = `fortinet` |
| HPE ProCurve | `hp_procurve` | Set platform `network_driver` = `hp_procurve` |

**Adding New Platforms:**
1. Verify the platform is supported by Netmiko
2. Create or edit the platform in Nautobot
3. Set the `network_driver` field to the corresponding Netmiko device type
4. No app restart or code changes required

## Integration Points

### From the App to Other Systems

#### Network Devices

**Connection Method and Protocol:**
- **SSH Connectivity**: All device communication occurs over SSH using the Netmiko library
- **Connection Targets**: Uses device primary IP addresses or device names for connection establishment
- **Authentication**: Retrieves credentials from device-assigned secrets groups automatically

**Data Flow and Communication:**
- **Command Transmission**: Commands are sent to devices through established SSH sessions
- **Output Collection**: Command output is captured and returned to Nautobot for processing and storage
- **Session Management**: Automatic connection establishment, command execution, and clean disconnection
- **Configuration Mode Handling**: Automatic entry into configuration mode when required for configuration changes

**Error Handling and Reliability:**
- **Connection Monitoring**: Real-time monitoring of connection status and command execution
- **Failure Detection**: Automatic detection and reporting of connection failures, authentication errors, and command execution problems
- **Detailed Logging**: Comprehensive logging of all device interactions for troubleshooting and audit purposes
- **Per-Device Results**: Individual result tracking for each target device with detailed error reporting

#### Nautobot Core Systems

**Device Inventory Integration:**
- **DCIM Models**: Reads device information from Nautobot's Device Configuration and Inventory Management models
- **Device Properties**: Accesses device names, primary IP addresses, platform assignments, and location data
- **Relationship Mapping**: Utilizes device relationships for secrets group assignments and platform driver selection

**Platform Management Integration:**
- **Platform Definitions**: Uses Nautobot platform records to determine appropriate connection drivers
- **Driver Mapping**: Maps platform `network_driver` field values to corresponding Netmiko device types
- **Dynamic Driver Selection**: Automatically selects appropriate drivers based on device platform assignments

**Secrets Management Integration:**
- **Secrets Groups**: Retrieves device credentials from assigned Nautobot secrets groups
- **Credential Security**: Leverages Nautobot's encrypted secrets storage for secure credential management
- **Dynamic Credential Retrieval**: Automatically retrieves appropriate credentials based on device secrets group assignments

**Location and Organizational Data:**
- **Location Hierarchy**: Accesses Nautobot's location hierarchy for location-based device filtering
- **Organizational Structure**: Utilizes site, building, and rack relationships for precise device targeting
- **Bulk Operations**: Enables location-based bulk operations across device groups

**Job Framework Integration:**
- **Job Execution System**: Full integration with Nautobot's job execution framework for user interface and progress monitoring
- **Result Storage**: Job results are stored within Nautobot's job result system for historical tracking and analysis
- **Progress Monitoring**: Real-time job progress updates through Nautobot's job monitoring interface
- **User Access Control**: Leverages Nautobot's user permissions system for job execution access control

### From Other Systems to the App

#### Nautobot API Integration
The app can be triggered through Nautobot's REST API:

## API Endpoints

The Device Broker app utilizes Nautobot's standard API endpoints and does not expose custom API endpoints. However, it can be controlled programmatically through Nautobot's existing APIs:

### Job Execution via API

Device Broker jobs can be executed programmatically using Nautobot's Jobs API:

**Endpoint**: `POST /api/extras/jobs/{job_id}/run/`

**Authentication**: Standard Nautobot API authentication (Token or Session)

**Request Parameters**:
- `devices`: List of device UUIDs (optional)
- `platform`: Platform UUID for platform-based filtering (optional)  
- `location`: Location UUID for location-based filtering (optional)
- `config_mode`: Boolean for configuration mode (required)
- `commands`: Multi-line string containing commands to execute (required)

### Device Management APIs

The app leverages these existing Nautobot APIs for device information:

**Device Information**: `GET /api/dcim/devices/`
- Retrieves device inventory data including names, IPs, platforms, and locations
- Used for device selection and connection target determination

**Platform Information**: `GET /api/dcim/platforms/`
- Accesses platform definitions and network_driver field values
- Used for driver selection and platform-based filtering

**Location Information**: `GET /api/dcim/locations/`
- Retrieves location hierarchy and organizational data
- Used for location-based device filtering and targeting

### Secrets Management APIs

**Secrets Groups**: `GET /api/extras/secrets-groups/`
- Accesses secrets group information and device assignments
- Used for credential retrieval and authentication

**Note**: Direct secrets access is handled internally by the app and is not exposed through external APIs for security reasons.

### Example API Usage

**Executing a Device Broker Job via API:**

```bash
curl -X POST \
  'https://nautobot.example.com/api/extras/jobs/device-broker-job/run/' \
  -H 'Authorization: Token YOUR_API_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
    "platform": "platform-uuid-here",
    "config_mode": false,
    "commands": "show version\nshow interfaces status"
  }'
```

**Python Example:**

```python
import requests

# Example: Trigger Device Broker job via API
job_data = {
    "devices": ["device-uuid-1", "device-uuid-2"],
    "commands": "show version\nshow interfaces",
    "config_mode": False
}

response = requests.post(
    "https://nautobot.example.com/api/extras/jobs/device-broker-job/run/",
    headers={"Authorization": "Token your-api-token"},
    json=job_data
)
```

**Retrieving Job Results:**

```bash
curl -X GET \
  'https://nautobot.example.com/api/extras/job-results/{job-result-id}/' \
  -H 'Authorization: Token YOUR_API_TOKEN'
```

### Integration Patterns

#### Automation Platform Integration
- **CI/CD Pipelines**: Jobs can be triggered from automation pipelines for infrastructure validation
- **Monitoring Systems**: External monitoring can trigger diagnostic commands based on alerts
- **Change Management**: Integration with change management workflows for pre/post change validation

## System Requirements

### Server Requirements
- **Operating System**: Linux (recommended), macOS, or Windows
- **Python Version**: 3.9+ (as specified in pyproject.toml)
- **Memory**: Dependent on number of concurrent device connections
- **Network**: Stable network connectivity to target devices

### Nautobot Requirements
- **Minimum Version**: 2.3.1
- **Maximum Version**: 2.9999 (current development constraint)
- **Required Features**: Jobs framework, Secrets management, Device models

### Network Requirements
- **Connectivity**: SSH connectivity from Nautobot server to target devices
- **DNS/Name Resolution**: Ability to resolve device hostnames (if using hostnames)
- **Latency**: Reasonable network latency for responsive command execution
- **Bandwidth**: Minimal bandwidth requirements for command/response traffic

## Security Considerations

### Credential Management
- Credentials are stored securely in Nautobot's secrets system
- No credentials are logged or stored in job output
- Device passwords are retrieved only when needed for connections

### Network Security
- All device communication occurs over SSH (encrypted)
- No plain-text protocols are used by default
- Firewall rules should restrict SSH access to only necessary sources

### Access Control
- Job execution is controlled by Nautobot's user permissions
- Users must have appropriate job execution permissions
- Device access is controlled through secrets group assignments

## API Endpoints

The Device Broker app utilizes standard Nautobot API endpoints:

### Device Management
- `GET /api/dcim/devices/` - Retrieve device information
- `GET /api/dcim/platforms/` - Retrieve platform information
- `GET /api/dcim/locations/` - Retrieve location information

### Secrets Management
- `GET /api/extras/secrets/` - Retrieve secret information (with appropriate permissions)

### Job Execution
- `POST /api/extras/jobs/{job-slug}/run/` - Execute Device Broker job
- `GET /api/extras/job-results/` - Retrieve job execution results

### Example API Usage

```bash
# Execute Device Broker job via curl
curl -X POST \
  https://nautobot.example.com/api/extras/jobs/device-broker-job/run/ \
  -H "Authorization: Token your-api-token" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "devices": [1, 2, 3],
      "commands": "show version\nshow interfaces",
      "config_mode": false
    }
  }'
```

## Troubleshooting External Connectivity

### Common Network Issues
- **SSH Connection Refused**: Verify SSH service is running on target devices
- **Connection Timeout**: Check network connectivity and firewall rules
- **Authentication Failure**: Verify credentials in secrets groups
- **DNS Resolution**: Ensure device hostnames resolve correctly

### Diagnostic Commands
```bash
# Test SSH connectivity from Nautobot server
ssh username@device-ip

# Test network connectivity
ping device-ip
telnet device-ip 22

# Check DNS resolution
nslookup device-hostname
```
