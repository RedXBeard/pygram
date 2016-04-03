# encoding: utf-8

import logging
from datetime import datetime

from pygram.app import PyGramApp

logger = logging.getLogger("main")

if __name__ == "__main__":
    # from run import main
    logging.basicConfig(filename="./log/pygram-{}.log".format(datetime.now().date()))
    # sys.exit(main())
    PyGramApp().run()
