import logging

import uvicorn

from src.app import app

uvicorn.run(app, log_level=logging.DEBUG)
