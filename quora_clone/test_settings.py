"""
Settings for running tests without Elasticsearch.
"""
import sys
from .settings import *

# Override settings for testing
if 'test' in sys.argv:
    # Remove Elasticsearch apps during testing
    INSTALLED_APPS = [app for app in INSTALLED_APPS if 'elasticsearch' not in app.lower()]
    
    # Use in-memory SQLite database for testing
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }
    
    # Disable Elasticsearch settings
    ELASTICSEARCH_DSL = {}
    ELASTICSEARCH_DSL_AUTO_REFRESH = False
    
    # Disable logging during tests
    LOGGING_CONFIG = None
    
    # Use Django's built-in password hasher for faster tests
    PASSWORD_HASHERS = [
        'django.contrib.auth.hashers.MD5PasswordHasher',
    ]
    
    # Disable migrations for faster tests
    class DisableMigrations:
        def __contains__(self, item):
            return True
        
        def __getitem__(self, item):
            return None
    
    MIGRATION_MODULES = DisableMigrations()