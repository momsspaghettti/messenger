import logging
import time
from traceback import format_tb
from typing import Optional


class TimerErrorSignal:
    def __init__(self):
        self.error = False


class Timer:
    def __init__(self, logger: logging.Logger, action_description: str,
                 error_signal: Optional[TimerErrorSignal] = None):
        self.logger = logger
        self.action_description = action_description
        self.start = None
        self.error_signal = error_signal

    def enter(self):
        self.start = time.process_time()
        return self

    def exit(self, exc_type, exc_val, exc_tb):
        elapsed = time.process_time() - self.start
        action_end = 'SUCCESS' \
            if exc_val is None and (self.error_signal is None or self.error_signal.error is False) \
            else f'ERROR ({exc_type}: {exc_val} at {format_tb(exc_tb)})' if exc_val is not None else 'ERROR'
        self.logger.info(
            f'Action {self.action_description} ended with {action_end}. Elapsed: {elapsed}')

    def __enter__(self):
        return self.enter()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.exit(exc_type, exc_val, exc_tb)

    async def __aenter__(self):
        return self.enter()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.exit(exc_type, exc_val, exc_tb)
