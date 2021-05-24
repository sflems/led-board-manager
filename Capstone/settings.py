"""
Django settings for Capstone project.

Generated by 'django-admin startproject' using Django 3.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import re, os, pytz
from secret_key_generator import secret_key_generator
from django.core.validators import MaxValueValidator, MinValueValidator, MaxLengthValidator

# SECURITY WARNING: keep the secret key used in production secret!
# secret_key_generator: https://pypi.org/project/secret-key-generator/
# This checks if a secret key is present in a .secret.txt file, and if not it generates one. Should be a good solution for local installs/dev use.
SECRET_KEY = secret_key_generator.generate()

# Get Pi's Configured Timezone. Fallback to 'America/Toronto'.
def pi_tz():
    if os.path.isfile("/etc/timezone"):
        with open("/etc/timezone", "r") as f:
            line = f.read().strip()
            while line in pytz.common_timezones:
                return line
    return 'America/Toronto'


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Activates testing mode: Uses static configs/schmea for unittest purposes. Uses `testing/` directory.
TEST_MODE = False

# Get current version from file
def sb_version():
    with open(os.path.join(BASE_DIR, "VERSION"), "r") as v:
        txt = v.read()
        while re.search(r'[v][0-9][\.][0-9]{1,2}[\.][0-9]{1,2}', txt) is not None:
            return txt.rstrip()


VERSION = sb_version()

# Allows server to be hosted on local subnet with unrestricted IPs. Make sure your firewall is accepting local network traffic only!!!
# This can be modified for your local subnet i.e. for subnet 192.168.0.0/16:
# ALLOWED_HOSTS = ['192.168.{}.{}'.format(i,j) for i in range(256) for j in range(256)]
ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'whitenoise.runserver_nostatic',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'corsheaders',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #'constance',
    'scoreboard.apps.CustomConstance',
    'constance.backends.database',
    'scoreboard',
    'rest_framework',
    'bootstrap4',
    'crispy_forms',
    'django_jsonforms',
    'prettyjson',
]

# These paths can be hard coded for specific usage or as fix if server breaks on change.
scoreboard_path = os.path.dirname(BASE_DIR) + "/nhl-led-scoreboard"
gui_path = os.path.dirname(BASE_DIR) + "/led-board-manager"

# Admin Field Modifcations go here.
CONSTANCE_ADDITIONAL_FIELDS = {
    'monitor_min': ['django.forms.IntegerField', {
        "validators": [MinValueValidator(5)]
    }],
    'gpio': ['django.forms.IntegerField', {
        "validators": [MaxValueValidator(4)]
    }],
    'parallel': ['django.forms.IntegerField', {
        "validators": [MaxValueValidator(3)]
    }],
    'scanning': ['django.forms.IntegerField', {
        "validators": [MaxValueValidator(1)]
    }],
    'rgb': ['django.forms.CharField', {
        "validators": [MaxLengthValidator(3)]
    }],
    'row_addr': ['django.forms.IntegerField', {
        "validators": [MaxValueValidator(1)]
    }],
    'hat_choices': ['django.forms.fields.ChoiceField', {
        'widget': 'django.forms.Select',
        'choices': (("regular", "regular"), ("adafruit-hat", "adafruit-hat"), ("adafruit-hat-pwm", "adafruit-hat-pwm"))
    }],
    'multiplexing': ['django.forms.fields.ChoiceField', {
        'widget': 'django.forms.Select',
        'choices': (
            (0, "regular"),
            (1, "strip"),
            (2, "checker"),
            (3, "spiral"),
            (4, "Z-strip"),
            (5, "ZnMirrorZStripe"),
            (6, "coreman"),
            (7, "Kaler2Scan"),
            (8, "ZStripeUneven")
        )
    }],

    'good_slug': ['django.forms.SlugField', {}],

    'good_url': ['django.forms.URLField', {}],

    'disabled': ['django.forms.CharField', {
        "disabled": True
    }],
}

CONSTANCE_CONFIG = {
    'GUI_DIR': (gui_path, 'Path to GUI Directory', 'disabled'),
    'MONITOR_INTERVAL': (10, 'Resource monitor system ping interval in seconds.', 'monitor_min'),
    'SCOREBOARD_DIR': (scoreboard_path, 'Path to NHL LED Scoreboard Directory. Change in Capstone/settings.py', 'disabled'),
    'SUPERVISOR_PROGRAM_NAME': ('scoreboard', 'ie. [program:scoreboard] from /etc/supervisor/conf.d/scoreboard.conf', 'good_slug'),
    'SUPERVISOR_GUI_NAME': ('led-board-manager', 'ie. [program:scoreboard-webgui] from /etc/supervisor/conf.d/scoreboard-webgui.conf', 'good_slug'),

    # Flags for the Scoreboard Process
    'LED_ROWS': (32, '16 for 16x32, 32 for 32x32 and 64x32.', int),
    'LED_COLS': (64, 'Panel columns. Typically 32 or 64.', int),
    'LED_CHAIN': (1, 'Daisy_chained boards.', int),
    'LED_PARALLEL': (1, 'For Plus_models or RPi2: parallel chains. 1..3.', 'parallel'),
    'LED_PWM_BITS': (11, 'Bits used for PWM. Range 1..11.', int),
    'LED_PWM_DITHER_BITS': (0, 'Time dithering of lower bits (Default: 0)', int),
    'LED_BRIGHTNESS': (80, 'Sets brightness level. Range: 1..100.', int),
    'LED_GPIO_MAPPING': ('adafruit-hat', 'Hardware Mapping: regular, adafruit-hat, adafruit-hat-pwm', 'hat_choices'),
    'LED_SCAN_MODE': (1, 'Progressive or interlaced scan. 0 = Progressive, 1 = Interlaced.', 'scanning'),
    'LED_PWM_LSB_NANOSECOND': (130, 'Base time-unit for the on-time in the lowest significant bit in nanoseconds.', int),
    'LED_SHOW_REFRESH': (False, 'Shows the current refresh rate of the LED panel.', bool),
    'LED_LIMIT_REFRESH': (0, 'Limit refresh rate to this frequency in Hz.', int),
    'LED_SLOWDOWN_GPIO': (2, 'Slow down writing to GPIO. Range: 0..4.', 'gpio'),
    'LED_NO_HARDWARE_PULSE': (False, 'Dont use hardware pin-pulse generation.', bool),
    'LED_RGB_SEQUENCE': ('RGB', ' Switch if your matrix has led colors swapped.', 'rgb'),
    'LED_PIXEL_MAPPER': ('', 'Apply pixel mappers. Optional params after a colon e.g. "U-mapper;Rotate:90"', str),
    'LED_ROW_ADDR_TYPE': (0, '0 = default; 1 = AB-addressed panels.', 'row_addr'),
    'LED_MULTIPLEXING': (
        0,
        'Multiplexing type: 0 = direct; 1 = strip; 2 = checker; 3 = spiral; 4 = Z-strip; 5 = ZnMirrorZStripe; 6 = coreman; 7 = Kaler2Scan; 8 = ZStripeUneven.',
        'multiplexing'
    ),
    'TERMINAL_MODE': (False, 'Enable terminal mode for testing.', bool),
    'TESTING_MODE': (False, "Allow to put use a loop in the renderer to do testing. For Development only", bool),
    'TESTSCCHAMPIONS': (False, "A flag to test the stanley cup champions board. Put your team's ID.", bool),
    'TEST_GOAL_ANIMATION': (False, "A flag to test the goal animation.", bool),
    'GHTOKEN': ("", 'Github API token for doing update checks.', str),
    'UPDATECHECK': (True, 'Enable update check.', bool),
    'UPDATE_REPO': ('https://github.com/riffnshred/nhl-led-scoreboard', 'Enable update check.', 'good_url'),
}

CONSTANCE_CONFIG_FIELDSETS = {
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
    'WebGUI Configuration': (
        'GUI_DIR',
        'MONITOR_INTERVAL',
        'SCOREBOARD_DIR',
        'SUPERVISOR_PROGRAM_NAME',
        'SUPERVISOR_GUI_NAME',
    ),
}

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
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
                'scoreboard.context_processors.version',
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

# TO DO: Need a function here to automagically pull TZ from timedatectl shell command
TIME_ZONE = pi_tz()

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

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny'
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ]
}

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
]
