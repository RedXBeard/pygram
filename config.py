import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

TELEGRAM_CLI_PATH = ""
PUBKEY_FILE = os.path.join(PROJECT_ROOT, 'pubkey.pub')
try:
    from config_local import *
except:
    pass
