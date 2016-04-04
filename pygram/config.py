import os

PACKAGE_ROOT = os.path.dirname(os.path.abspath(__file__))

TELEGRAM_CLI_PATH = os.path.join(os.path.expanduser('~'),".tg/bin/telegram-cli")
PUBKEY_FILE = os.path.join(PACKAGE_ROOT, 'pubkey.pub')
try:
    from pygram.config_local import *
except ImportError:
    pass
