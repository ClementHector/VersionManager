import re
from copy import deepcopy

def save_previous_version(func):
    def wrapper(self, *args, **kwargs):
        if not hasattr(self, "previous_versions"):
            self.previous_versions = [deepcopy(self)]
        else:
            self.previous_versions.append(deepcopy(self))
        return func(self, *args, **kwargs)
    return wrapper

class VersionManager:
    """Version Manager class for semantic versioning."""
    RE_STR = r'^(?P<major>\d+)(?:\.(?P<minor>\d+)(?:\.(?P<patch>\d+))?)?'
    _REGEX = re.compile(RE_STR, re.VERBOSE)

    def __init__(self, version: str = "0.0.1") -> None:
        self._parse_version(version)

    def __repr__(self) -> str:
        return f"< VersionManager MAJOR:{self._major} MINOR:{self._minor} " \
            f"PATCH:{self._patch} >"

    def _parse_version(self, version: str) -> None:
        match = re.match(self._REGEX, version)
        if not match:
            raise SemVerNotValid

        _version_dict: dict = match.groupdict(0)
        self._version: str = version
        self._major: int = int(_version_dict["major"])
        self._minor: int = int(_version_dict.get("minor"))
        self._patch: int = int(_version_dict.get("patch"))

    @save_previous_version
    def major(self) -> 'VersionManager':
        """Increments major version by 1 and resets minor and patch to 0.
        returns:
            VersionManager: current version"""
        self._major += 1
        self._minor = 0
        self._patch = 0
        return self

    @save_previous_version
    def minor(self) -> 'VersionManager':
        """Increments minor version by 1 and resets patch to 0.
        returns:
            VersionManager: current version"""
        self._minor += 1
        self._patch = 0
        return self

    @save_previous_version
    def patch(self) -> 'VersionManager':
        """Increments patch version by 1.
        returns:
            VersionManager: current version"""
        self._patch += 1
        return self

    def rollback(self) -> 'VersionManager':
        """Rolls back to previous version.
        returns:
            VersionManager: current version"""
        if not self.previous_versions:
            raise Exception("Cannot rollback!")

        previous_version = self.previous_versions.pop()

        self._major = previous_version._major
        self._minor = previous_version._minor
        self._patch = previous_version._patch

        return self

    def release(self) -> str:
        """Returns the current version.
        returns:
            str: current version"""
        return f"{self._major}.{self._minor}.{self._patch}"


class SemVerNotValid(Exception):
    """Exception raised for errors in the input.
    """
    def __init__(self, message: str = "Error occurred while parsing version!"):
        self.message = message
        super().__init__(self.message)

