

class DefaultConfiguration(object):
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'format': '%(asctime)s %(pathname)s:%(lineno)d %(name)s %(levelname)s: %(message)s'
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'NOTSET',
                'formatter': 'default'
            },
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'NOTSET',
                "filename": "commanderpy.log",
                "maxBytes": 10485760,
                "backupCount": 2,
                "encoding": "utf8"
            }
        },
        'loggers': {
            'oauthlib': {
                'handlers': ['console', 'file'],
                'level': 'WARNING',
            },
            'pika': {
                'handlers': ['console', 'file'],
                'level': 'WARNING',
            },
            'requests': {
                'handlers': ['console', 'file'],
                'level': 'WARNING',
            },
            'requests_oauthlib': {
                'handlers': ['console', 'file'],
                'level': 'WARNING',
            },
            'tweepy': {
                'handlers': ['console', 'file'],
                'level': 'WARNING',
            }
        },

        'root': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',

        }

    }