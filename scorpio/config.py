DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'scorpio-db',
        'PORT': 5432,
    }
}

ELASTICSEARCH = {
    "host": "elasticsearch",
}

ALLOWED_HOSTS = ['localhost', 'scorpio-web']
