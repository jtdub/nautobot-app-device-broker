"""App declaration for device_broker."""

# Metadata is inherited from Nautobot. If not including Nautobot in the environment, this should be added
from importlib import metadata

from nautobot.apps import NautobotAppConfig

__version__ = metadata.version(__name__)


class DeviceBrokerConfig(NautobotAppConfig):
    """App configuration for the device_broker app."""

    name = "device_broker"
    verbose_name = "Device Broker"
    version = __version__
    author = "James Williams"
    description = "Platform-agnostic network device command execution and automation toolkit for Nautobot."
    base_url = "device-broker"
    required_settings = []
    min_version = "2.3.1"
    max_version = "2.9999"
    default_settings = {}
    caching_config = {}
    docs_view_name = "plugins:device_broker:docs"


config = DeviceBrokerConfig  # pylint:disable=invalid-name
