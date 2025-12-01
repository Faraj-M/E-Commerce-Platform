from importlib import import_module
from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'web']

try:
    import_module('debug_toolbar')
except ImportError:
    debug_toolbar_available = False
else:
    debug_toolbar_available = True

if debug_toolbar_available:
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
    INTERNAL_IPS = ['127.0.0.1']
