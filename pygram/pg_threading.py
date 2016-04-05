import asyncio
import threading

from pytg.exceptions import NoResponse, IllegalResponseException, ConnectionError


class PGThread(threading.Thread):
    def run(self):
        try:
            if self._target:
                self._target(*self._args, **self._kwargs)
        except (asyncio.TimeoutError, GeneratorExit, KeyboardInterrupt,
                TypeError, RuntimeError, NoResponse, IllegalResponseException,
                ConnectionError):
            pass
        finally:
            del self._target, self._args, self._kwargs
