import os
from datadog import initialize, api


_INIT = False

def init_api():
    global _INIT
    if _INIT:
        return
    APP_KEY = os.environ['DOG_APP_KEY']
    API_KEY = os.environ['DOG_API_KEY']
    initialize(app_key=APP_KEY, api_key=API_KEY)
    _INIT = True


init_api()
