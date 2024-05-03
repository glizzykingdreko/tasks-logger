import datetime
import threading
from typing import Any, Optional, Callable, Dict
from colorama import Fore, Style, init

# Initialize colorama to reset styles automatically after each print
init(autoreset=True)

class Logger:
    """
    A flexible, multi-level, and color-coded logging system designed to handle
    concurrent logging across different tasks and threads.

    Attributes:
        level (int): Minimum severity level of logs that will be printed to the console.
        file_level (int): Minimum severity level of logs that will be saved to a file.
        filename (Optional[str]): Name of the file where logs are saved, if any.
        format (str): The format string that defines the log message layout.
        colors (Dict[str, str]): Dictionary mapping each log level to a specific color.
        metadata (Dict[str, Any]): Dictionary storing arbitrary metadata for log formatting.
    """
    LEVELS: Dict[str, int] = {}
    DEFAULT_COLORS: Dict[str, str] = {}
    file_lock = threading.Lock()  # Lock for thread-safe file writing

    def __init__(self, level: str = 'INFO', file_level: str = 'INFO', filename: Optional[str] = None,
                 formatting: str = "{timestamp} {level}: {message}", colors: Optional[Dict[str, str]] = None, **metadata: Any):
        """Initialize the Logger with default levels, file logging settings, and optional metadata."""
        self.setup_default_levels()
        self.level = self.LEVELS.get(level.upper(), 20)
        self.file_level = self.LEVELS.get(file_level.upper(), 20)
        self.filename = filename
        self.format = formatting
        self.colors = colors if colors else self.DEFAULT_COLORS
        self.metadata = metadata

    @classmethod
    def setup_default_levels(cls):
        """Setup default log levels with corresponding colors if they have not been explicitly set."""
        defaults = {
            'DEBUG': (10, Fore.BLUE),
            'INFO': (20, Fore.CYAN),
            'WARNING': (30, Fore.YELLOW),
            'ERROR': (40, Fore.RED),
            'CRITICAL': (50, Fore.RED),
            'SUCCESS': (25, Fore.GREEN)
        }
        for level, (severity, color) in defaults.items():
            if level not in cls.LEVELS:
                cls.add_level(level, severity, color)

    @classmethod
    def add_level(cls, name: str, severity: int, color: Optional[str] = None):
        """Add or modify a logging level with an optional color."""
        cls.LEVELS[name.upper()] = severity
        if color:
            cls.DEFAULT_COLORS[name.upper()] = color
        if not hasattr(cls, name.lower()):
            setattr(cls, name.lower(), cls._make_log_method(name.upper()))

    @staticmethod
    def _make_log_method(level: str) -> Callable:
        """Dynamically create a logging method for a specified level."""
        def log_method(self, message: str, **kwargs: Any):
            self.log(message, level, **kwargs)
        log_method.__name__ = level.lower()
        return log_method

    def log(self, message: str, level: str, **kwargs: Any):
        """Log a message at a given level, formatted and output appropriately based on configuration."""
        if self.LEVELS[level] < self.level:
            return
        metadata = {**self.metadata, **kwargs}
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_message = self.format.format(
            level=level,
            message=message,
            timestamp=timestamp,
            **metadata
        )
        self._write(formatted_message, level)

    def _write(self, message: str, level: str):
        """Write the formatted message to either a file or stdout with appropriate coloring, in a thread-safe manner."""
        color = self.colors.get(level, '')
        if self.filename and self.LEVELS[level] >= self.file_level:
            with self.file_lock:
                with open(self.filename, 'a') as f:
                    f.write(message + '\n')
        if self.LEVELS[level] >= self.level:
            with self.file_lock:
                print(f"{color}{message}{Style.RESET_ALL}")

    # Pre-defined methods for common log levels
    def debug(self, message: str, **kwargs: Any):
        """Log a debug message."""
        self.log(message, 'DEBUG', **kwargs)

    def info(self, message: str, **kwargs: Any):
        """Log an info message."""
        self.log(message, 'INFO', **kwargs)

    def warning(self, message: str, **kwargs: Any):
        """Log a warning message."""
        self.log(message, 'WARNING', **kwargs)

    def error(self, message: str, **kwargs: Any):
        """Log an error message."""
        self.log(message, 'ERROR', **kwargs)

    def critical(self, message: str, **kwargs: Any):
        """Log a critical message."""
        self.log(message, 'CRITICAL', **kwargs)

    def success(self, message: str, **kwargs: Any):
        """Log a success message."""
        self.log(message, 'SUCCESS', **kwargs)
