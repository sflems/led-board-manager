"""
Django settings for Capstone project.

Generated by 'django-admin startproject' using Django 3.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from secret_key_generator import secret_key_generator

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# secret_key_generator: https://pypi.org/project/secret-key-generator/
# This checks if a secret key is present in a .secret.txt file, and if not it generates one. Should be a good solution for local installs/dev use.
SECRET_KEY = secret_key_generator.generate()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Activates demo mode: Uses static configs/schmea for CS50 demo purposes.
DEMO_CS50 = False

# Allows server to be hosted on local subnet with unrestricted IPs. Make sure your firewall is accepting local network traffic only!!!
# This can be modified for your local subnet. See below.
ALLOWED_HOSTS = ['*']

# i.e. for subnet 192.168.0.0/16
# ALLOWED_HOSTS = ['192.168.{}.{}'.format(i,j) for i in range(256) for j in range(256)]


# Application definition

INSTALLED_APPS = [
    'whitenoise.runserver_nostatic',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'constance',
    'constance.backends.database',
    'scoreboard',
    'bootstrap4',
    'crispy_forms',
    'django_jsonforms',
    'prettyjson',
]

# These paths can be hard coded for specific usage or as fix if server breaks on change.
scoreboard_path = os.path.dirname(BASE_DIR) + "/nhl-led-scoreboard"
gui_path = os.path.dirname(BASE_DIR) + "/nhl-led-scoreboard-webgui"

CONSTANCE_CONFIG = {
    'GUI_DIR': (gui_path, 'Path to GUI Directory'),
    'MONITOR_INTERVAL': (10, 'Resource monitor system ping interval in seconds.', int),
    'SCOREBOARD_DIR': (scoreboard_path, 'Path to NHL LED Scoreboard Directory'),
    'SUPERVISOR_PROGRAM_NAME': ('scoreboard', 'ie. [program:scoreboard] from /etc/supervisor/conf.d/scoreboard.conf'),
    'SUPERVISOR_GUI_NAME': ('scoreboard-webgui', 'ie. [program:scoreboard-webgui] from /etc/supervisor/conf.d/scoreboard-webgui.conf'),

    # Flags for the Scoreboard Process
    'LED_ROWS': (32, '16 for 16x32, 32 for 32x32 and 64x32.', int),
    'LED_COLS': (64, 'Panel columns. Typically 32 or 64.', int),
    'LED_CHAIN': (1, 'Daisy_chained boards.', int),
    'LED_PARALLEL': (1, 'For Plus_models or RPi2: parallel chains. 1..3.', int),
    'LED_PWM_BITS': (11, 'Bits used for PWM. Range 1..11.', int),
    'LED_PWM_DITHER_BITS': (0, 'Time dithering of lower bits (Default: 0)', int),
    'LED_BRIGHTNESS': (80, 'Sets brightness level. Range: 1..100.', int),
    'LED_GPIO_MAPPING': ('adafruit-hat', 'Hardware Mapping: regular, adafruit-hat, adafruit-hat-pwm', str),
    'LED_SCAN_MODE': (1, 'Progressive or interlaced scan. 0 = Progressive, 1 = Interlaced.', int),
    'LED_PWM_LSB_NANOSECOND': (130, 'Base time-unit for the on-time in the lowest significant bit in nanoseconds.', int),
    'LED_SHOW_REFRESH': (False, 'Shows the current refresh rate of the LED panel.', bool),
    'LED_LIMIT_REFRESH': (0, 'Limit refresh rate to this frequency in Hz.', int),
    'LED_SLOWDOWN_GPIO': (2, 'Slow down writing to GPIO. Range: 0..4.', int),
    'LED_NO_HARDWARE_PULSE': (False, 'Dont use hardware pin-pulse generation.', bool),
    'LED_RGB_SEQUENCE': ('RGB', ' Switch if your matrix has led colors swapped.', str),
    'LED_PIXEL_MAPPER': ('', 'Apply pixel mappers. Optional params after a colon e.g. "U-mapper;Rotate:90"', str),
    'LED_ROW_ADDR_TYPE': (0, '0 = default; 1 = AB-addressed panels.', int),
    'LED_MULTIPLEXING': (0, 'Multiplexing type: 0 = direct; 1 = strip; 2 = checker; 3 = spiral; 4 = Z-strip; 5 = ZnMirrorZStripe; 6 = coreman; 7 = Kaler2Scan; 8 = ZStripeUneven.', int),
    'TERMINAL_MODE': (False, 'Enable terminal mode for testing.', bool),
    'TESTING_MODE': (False, "Allow to put use a loop in the renderer to do testing. For Development only", bool),
    'TESTSCCHAMPIONS': ("", "A flag to test the stanley cup champions board. Put your team's ID."),
    'TEST_GOAL_ANIMATION': (False, "A flag to test the goal animation.", bool),
    'GHTOKEN': ("", 'Github API token for doing update checks.', str),
    'UPDATECHECK': (True, 'Enable update check.', bool),
    'UPDATE_REPO': ('https://github.com/riffnshred/nhl-led-scoreboard', 'Enable update check.', str),



}

CONSTANCE_CONFIG_FIELDSETS = {
    'WebGUI Configuration': (
        'GUI_DIR',
        'MONITOR_INTERVAL',
        'SCOREBOARD_DIR',
        'SUPERVISOR_PROGRAM_NAME',
        'SUPERVISOR_GUI_NAME',
    ),
    'Scoreboard Flags': {
        'fields': (
            'LED_ROWS',
            'LED_COLS',
            'LED_BRIGHTNESS',
            'LED_GPIO_MAPPING',
            'LED_SLOWDOWN_GPIO',
            'LED_SHOW_REFRESH',
            'LED_LIMIT_REFRESH',
            'LED_CHAIN',
            'LED_PARALLEL',
            'LED_PWM_BITS',
            'LED_PWM_DITHER_BITS',
            'LED_SCAN_MODE',
            'LED_PWM_LSB_NANOSECOND',
            'LED_NO_HARDWARE_PULSE',
            'LED_RGB_SEQUENCE',
            'LED_PIXEL_MAPPER',
            'LED_ROW_ADDR_TYPE',
            'LED_MULTIPLEXING',
            'TERMINAL_MODE',
            'TESTING_MODE',
            'TESTSCCHAMPIONS',
            'TEST_GOAL_ANIMATION',
            'GHTOKEN',
            'UPDATECHECK',
            'UPDATE_REPO',
        ),
        'collapse': False
    },
}

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Capstone.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'constance.context_processors.config',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Capstone.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

AUTH_USER_MODEL = "scoreboard.User"

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Corrects the default login redirect from the django defaults
LOGIN_URL = 'login'


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Vancouver'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') 
STATIC_URL = '/static/'
STATIC_FILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Dummy cache used for data intensive sites & development environments as per Django docs. Should be a good solution for this.
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}