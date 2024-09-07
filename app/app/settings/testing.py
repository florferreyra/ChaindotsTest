from environs import Env

env = Env()
env.read_env()

TESTING_MODE = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env.str("POSTGRES_DB"),
        "USER": env.str("POSTGRES_USER"),
        "PASSWORD": env.str("POSTGRES_PASSWORD"),
        "HOST": env.str("POSTGRES_HOST"),  # this should match the service name in your docker-compose.yml file
        "PORT": env.str("POSTGRES_PORT"),
    }
}

USE_TZ = False
