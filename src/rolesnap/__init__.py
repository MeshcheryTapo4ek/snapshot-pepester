from importlib.metadata import PackageNotFoundError, version

try:
    __version__: str = version("rolesnap")
except PackageNotFoundError:
    __version__ = "0.0.0"
