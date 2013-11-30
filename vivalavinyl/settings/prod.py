# Default Django settings for project.
from vivalavinyl.settings import * 

# Database #
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'vivalavinyl_new',
	'USER': 'vivalavinyl',
	'PASSWORD': 'wut@ngr00lz',
	'HOST': 'localhost',
	'PORT': '5432',
    }
}