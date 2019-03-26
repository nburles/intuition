from contextlib import contextmanager
import signal

@contextmanager
def signal_handler():
    orig_sigint_handler = signal.signal(signal.SIGINT, signal.SIG_IGN)
    try:
        yield
    finally:
        signal.signal(signal.SIGINT, orig_sigint_handler)

