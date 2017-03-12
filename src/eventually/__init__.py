from ._version import __version__

from ._deprecate import (
    getDeprecationWarningString,
    deprecated,
    deprecatedProperty,
    deprecatedModuleAttribute,
    DEPRECATION_WARNING_FORMAT,
    warnAboutFunction,
    getWarningMethod,
    setWarningMethod
)

all = [
    "getDeprecationWarningString",
    "deprecated",
    "deprecatedProperty",
    "deprecatedModuleAttribute",
    "DEPRECATION_WARNING_FORMAT",
    "warnAboutFunction",
    "getWarningMethod",
    "setWarningMethod",
    "__version__"
]
