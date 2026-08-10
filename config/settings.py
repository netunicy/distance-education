import os
from pathlib import Path
import cloudinary
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

def read_secret(file_name, default=None):
    try:
        base_dir = BASE_DIR / "config" / "secrets"
        with open(base_dir / file_name) as f:
            return f.read().strip()
    except FileNotFoundError:
        return default


SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY") or read_secret("secret_key.txt")

DEBUG = False
ALLOWED_HOSTS = [
    'distance-education.onrender.com',
    'turnonlearning.com',
    'www.turnonlearning.com',
    'localhost',
    '127.0.0.1',
]


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.sites',

    'cloudinary',

    'tinymce',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    'homepage.apps.HomepageConfig',
    'accounts.apps.AccountsConfig',
]
SITE_ID = 1
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Αν τρέχει στο Render (Production), συνδέσου στο Neon Postgres
DATABASE_URL = os.environ.get('DATABASE_URL') or read_secret ("d_b_url_neon.txt")

if DATABASE_URL:
    DATABASES['default'] = dj_database_url.config(
        default=DATABASE_URL,
        conn_max_age=600,
        ssl_require=True  # Το Neon ΑΠΑΙΤΕΙ SSL ακόμα και από localhost
    )


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Athens'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static",]
STATIC_ROOT = BASE_DIR / "staticfiles"

CLOUDINARY_CLOUD_NAME = (
    os.environ.get("CLOUDINARY_CLOUD_NAME")
    or read_secret("cloudinary_cloud_name.txt")
)

CLOUDINARY_API_KEY = (
    os.environ.get("CLOUDINARY_API_KEY")
    or read_secret("cloudinary_api_key.txt")
)

CLOUDINARY_API_SECRET = (
    os.environ.get("CLOUDINARY_API_SECRET")
    or read_secret("cloudinary_api_secret.txt")
)


cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET,
    secure=True,
)

CLOUDFLARE_ACCOUNT_ID = os.environ.get("CLOUDFLARE_ACCOUNT_ID") or read_secret ("cloudflare_account_id.txt")
CLOUDFLARE_API_TOKEN = os.environ.get("CLOUDFLARE_API_TOKEN") or read_secret ("cloudflare_api_token.txt")
CLOUDFLARE_STREAM_KEY_ID = (os.environ.get("CLOUDFLARE_STREAM_KEY_ID") or read_secret("cloudflare_stream_key_id.txt"))
CLOUDFLARE_STREAM_PRIVATE_KEY = (os.environ.get("CLOUDFLARE_STREAM_PRIVATE_KEY") or read_secret("cloudflare_stream_private_key.pem"))
CLOUDFLARE_STREAM_CUSTOMER_SUBDOMAIN = (os.environ.get("CLOUDFLARE_STREAM_CUSTOMER_SUBDOMAIN") or read_secret("cloudflare_stream_customer_subdomain.txt"))


# Προαιρετικές ρυθμίσεις για το allauth (αν χρησιμοποιείς το email για login)
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'optional'

# 1. Παίρνουμε την τιμή από το περιβάλλον ή το αρχείο
CLIENT_ID = os.environ.get("CLIENT_ID") or read_secret ("cliend_id_google_login.txt")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET") or read_secret ("cliend_secret_id_google_login.txt")
# Παρακάμπτει την ενδιάμεση οθόνη επιβεβαίωσης του allauth (3rdparty/signup)
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_LOGIN_ON_GET = True

# URL μετά από επιτυχημένο Login / Register
LOGIN_REDIRECT_URL = '/'  # ή '/dashboard/' ή όποιο path θέλεις

# URL μετά από Logout
LOGOUT_REDIRECT_URL = '/'

# 2. Τη βάζουμε στο SOCIALACCOUNT_PROVIDERS
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': CLIENT_ID,
            'secret': CLIENT_SECRET,
            'key': ''
        },
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# settings.py

if not DEBUG:
    # Ρυθμίσεις Ασφαλείας μόνο για Production (HTTPS)
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = "None"
    CSRF_COOKIE_SECURE = True
    CSRF_COOKIE_SAMESITE = "None"
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_AGE = 86400


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'bulk.smtp.mailtrap.io'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = 'api'
EMAIL_HOST_PASSWORD = os.environ.get("MAILTRAP_KEY") or read_secret ("mailtrap_key.txt")
DEFAULT_FROM_EMAIL = 'Turn On Learning <hello@turnonlearning.com>'
MAILTRAP_TOKEN = os.environ.get("MAILTRAP_KEY") or read_secret ("mailtrap_key.txt")

# settings.py
CSRF_TRUSTED_ORIGINS = [
    "https://www.turnonlearning.com",
    "https://turnonlearning.com",
    "https://distance-education.onrender.com",
]
TINYMCE_DEFAULT_CONFIG = {
    "height": 600,
    "width": 960,
    "language": "el",

    "plugins": (
        "advlist autolink lists link image charmap preview anchor "
        "searchreplace visualblocks code fullscreen insertdatetime media "
        "table help wordcount paste"
    ),

    "toolbar": (
        "undo redo | bold italic underline strikethrough | "
        "fontselect fontsizeselect formatselect | "
        "alignleft aligncenter alignright alignjustify | "
        "outdent indent | numlist bullist checklist | "
        "removeformat | link image media | "
        "fullscreen preview code"
    ),

    # -------------------------------
    # PIXEL FONT SIZES στο dropdown
    # -------------------------------
    "fontsize_formats": "10px 12px 14px 16px 18px 20px 22px 24px 26px 28px 30px 32px 36px 40px 48px",

    "style_formats": [
        {"title": "10px", "inline": "span", "styles": {"font-size": "10px"}},
        {"title": "12px", "inline": "span", "styles": {"font-size": "12px"}},
        {"title": "14px", "inline": "span", "styles": {"font-size": "14px"}},
        {"title": "16px", "inline": "span", "styles": {"font-size": "16px"}},
        {"title": "18px", "inline": "span", "styles": {"font-size": "18px"}},
        {"title": "20px", "inline": "span", "styles": {"font-size": "20px"}},
        {"title": "22px", "inline": "span", "styles": {"font-size": "22px"}},
        {"title": "24px", "inline": "span", "styles": {"font-size": "24px"}},
        {"title": "26px", "inline": "span", "styles": {"font-size": "26px"}},
        {"title": "28px", "inline": "span", "styles": {"font-size": "28px"}},
        {"title": "30px", "inline": "span", "styles": {"font-size": "30px"}},
        {"title": "32px", "inline": "span", "styles": {"font-size": "32px"}},
        {"title": "36px", "inline": "span", "styles": {"font-size": "36px"}},
        {"title": "40px", "inline": "span", "styles": {"font-size": "40px"}},
        {"title": "48px", "inline": "span", "styles": {"font-size": "48px"}},
    ],

    "formats": {
        "bold": {"inline": "strong", "remove": "all"},
        "italic": {"inline": "em", "remove": "all"},
        "underline": {"inline": "u", "remove": "all"},
        "strikethrough": {"inline": "del", "remove": "all"},
    },

    "forced_root_block": "p",
    "force_br_newlines": False,
    "force_p_newlines": True,

    "paste_as_text": True,

    "menubar": "file edit view insert format tools table help",
    "image_advtab": True,
    "branding": False,
    "toolbar_mode": "wrap",
    "contextmenu": "link image table",
}
