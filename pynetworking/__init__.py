# Import python libs
import warnings

# All salt related deprecation warnings should be shown once each!
warnings.filterwarnings(
    'once',  # Show once
    '',  # No deprecation message match
    DeprecationWarning,  # This filter is for DeprecationWarnings
    r'^(pynetworking|pynetworking\.(.*))$'  # Match module(s) 'pynetworking' and 'pynetworking.<whatever>'
)

# While we are supporting Python2.6, hide nested with-statements warnings
warnings.filterwarnings(
    'ignore',
    'With-statements now directly support multiple context managers',
    DeprecationWarning
)

from pynetworking.Device import Device
__username__ = Device.username

import inspect
__all__ = [name for name, obj in locals().items() if not (name.startswith('_') or inspect.ismodule(obj))]

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
