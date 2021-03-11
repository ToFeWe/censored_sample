from os import environ

SESSION_CONFIGS = [
    dict(
       name='truncated_reporting_BEST',
       display_name="truncated_reporting_BEST",
       num_demo_participants=10,
       treatment_list=['BEST'],
       app_sequence=['truncated_reporting']
    ),
    dict(
       name='truncated_reporting_FULL',
       display_name="truncated_reporting_FULL",
       num_demo_participants=10,
       treatment_list=['FULL'],
       app_sequence=['truncated_reporting']
    ),
    dict(
       name='truncated_reporting_RANDOM',
       display_name="truncated_reporting_RANDOM",
       num_demo_participants=10,
       treatment_list=['RANDOM'],
       app_sequence=['truncated_reporting']
    ),
    dict(
       name='truncated_reporting_CYCLE',
       display_name="truncated_reporting_CYCLE",
       num_demo_participants=10,
       app_sequence=['truncated_reporting']
    ),
    dict(
       name='truncated_reporting_PILOT',
       display_name="truncated_reporting_PILOT",
       num_demo_participants=10,
       treatment_list = ['FULL', 'BEST'],
       app_sequence=['truncated_reporting']
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1/15, participation_fee=4.00, doc=""
)

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'de'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'EUR'
USE_POINTS = True
POINTS_CUSTOM_NAME = "Taler"

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = 'pkx&mvj6=ilo_dw$00!-9%%qtpenwv0wcnsj1+%^o7#0$ne9=)'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']
