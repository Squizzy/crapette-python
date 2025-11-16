import logging
import inspect
from enum import Enum

# from datetime import datetime
from pathlib import Path
# from typing import Optional

from constants import TextColours

class DebugLevel(Enum):
    card = logging.WARNING
    cardstack = logging.WARNING
    client_game_comms = logging.WARNING
    client_game_state = logging.WARNING
    client_msg_decoder = logging.DEBUG
    client_msg_encoder = logging.WARNING
    client_network = logging.DEBUG
    client_pygame = logging.DEBUG
    client_ui_cards = logging.DEBUG
    client_ui_game_state = logging.DEBUG
    client_ui_stacks_layout = logging.DEBUG
    client_ui = logging.DEBUG
    constants = logging.WARNING
    deck = logging.WARNING
    game_logger = logging.WARNING
    network_messages = logging.WARNING
    player = logging.WARNING
    server_game_comms = logging.WARNING
    server_game_state = logging.WARNING
    server_msg_decoder = logging.WARNING
    server_msg_encoder = logging.WARNING
    server_network = logging.WARNING
    server_pygame = logging.WARNING
    stack_bin = logging.WARNING
    stack_crapette = logging.WARNING
    stack_foundation = logging.WARNING
    stack_remainder = logging.WARNING
    stack_tableau = logging.WARNING
    stacks = logging.WARNING

class LogColours:
    TIME = TextColours.GREY 
    DEBUG = TextColours.BRIGHT_CYAN
    INFO = TextColours.GREEN
    WARNING = TextColours.YELLOW
    ERROR = TextColours.ORANGE
    CRITICAL = TextColours.RED
    CALLER = TextColours.PURPLE

class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors"""
    
    log_time = LogColours.TIME + "%(asctime)s" + TextColours.RESET
    log_levels = {
        logging.DEBUG: LogColours.DEBUG + "%(levelname)s" + TextColours.RESET,
        logging.INFO: LogColours.INFO + "%(levelname)s" + TextColours.RESET,
        logging.WARNING: LogColours.WARNING + "%(levelname)s" + TextColours.RESET,
        logging.ERROR: LogColours.ERROR + "%(levelname)s " + TextColours.RESET,
        logging.CRITICAL: LogColours.CRITICAL + "%(levelname)s" + TextColours.RESET
    }
    log_message = "%(message)s"
    
    
    # FORMATS = {
    #     logging.DEBUG: TextColours.GREY + "%(asctime)s - %(levelname)s - %(message)s" + TextColours.RESET,
    #     logging.INFO: TextColours.BLUE + "%(asctime)s - %(levelname)s - %(message)s" + TextColours.RESET,
    #     logging.WARNING: TextColours.YELLOW + "%(asctime)s - %(levelname)s - %(message)s" + TextColours.RESET,
    #     logging.ERROR: TextColours.RED + "%(asctime)s - %(levelname)s - %(message)s" + TextColours.RESET,
    #     logging.CRITICAL: TextColours.RED + "%(asctime)s - %(levelname)s - %(message)s" + TextColours.RESET
    # }

    def format(self, record: logging.LogRecord):
        # global log_time, log_message
        log_fmt = f"{self.log_time} {self.log_levels.get(record.levelno)} {self.log_message}"
        # log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt="%Y/%m/%d %H:%M:%S")
        return formatter.format(record)


class GameLogger:
    
    def __init__(self, name: str, log_file: str | None = None, level: int = logging.WARNING) -> None:
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # Console handler with colours
        console_handler = logging.StreamHandler()
        # console_handler.setLevel(logging.DEBUG)
        console_handler.setLevel(level)
        console_handler.setFormatter(ColoredFormatter())
        self.logger.addHandler(console_handler)
        
        # file_handler = logging.FileHandler('game.log')
        # file_handler.setFormatter(formatter)
        # self.logger.addHandler(file_handler)
        # self.logger.info('Logger initialized')
                # File handler (no colors in file)
        if log_file:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s'
            ))
            self.logger.addHandler(file_handler)
    
    def _get_caller_info(self) -> str:
        """Get the caller's module and function name."""

        stack = inspect.stack()
        if len(stack) < 3:
            return "no stack for logging info"
        try:
            caller_frame = stack[2]
            module = caller_frame.frame.f_globals['__name__']
            function = caller_frame.function
            line_number = caller_frame.lineno
            return f"[{module}:{function}]:{line_number}"
        except Exception:
            return "no stack for logging info"

    
    def debug(self, message:str) -> None:
        caller = self._get_caller_info()
        log_caller = f"{LogColours.CALLER}{caller}{TextColours.RESET}"
        self.logger.debug(f"{log_caller} {message}")
        
    def info(self, message:str) -> None:
        caller = self._get_caller_info()
        log_caller = f"{LogColours.CALLER}{caller}{TextColours.RESET}"
        self.logger.info(f"{log_caller} {message}")
        
    def warning(self, message:str) -> None:
        caller = self._get_caller_info()
        log_caller = f"{LogColours.CALLER}{caller}{TextColours.RESET}"
        self.logger.warning(f"{log_caller} {message}")
        
    def error(self, message:str) -> None:
        caller = self._get_caller_info()
        log_caller = f"{LogColours.CALLER}{caller}{TextColours.RESET}"
        self.logger.error(f"{log_caller} {message}")
        
    def critical(self, message:str) -> None:
        caller = self._get_caller_info()
        log_caller = f"{LogColours.CALLER}{caller}{TextColours.RESET}"
        self.logger.critical(f"{log_caller} {message}")