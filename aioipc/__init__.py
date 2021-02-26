from collections import namedtuple

from aioipc.client import Client
from aioipc.server import Server
from aioipc.errors import *

__version__ = "1.0.1"

_VersionInfo = namedtuple("_VersionInfo", "major minor micro releaselevel serial")
version_info = _VersionInfo(major=1, minor=0, micro=1, releaselevel="final", serial=0)
