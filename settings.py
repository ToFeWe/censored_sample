from os import environ

SESSION_CONFIGS = [
   dict(
         name='SELF_2_x_BEST_FULL_BEST',
         display_name="SELF_2_x_BEST_FULL_BEST",
         num_demo_participants=50,
         use_browser_bots=False,
         expShortName='trunlot',
         expId=1616578277,
         treatment_list = ['FULL_BEST', 'BEST', 'BEST'],
         app_sequence=['truncated_reporting', 'quiz', 'payment']
      ),
   dict(
         name='BOT_2_x_BEST_FULL_BEST',
         display_name="BOT_2_x_BEST_FULL_BEST",
         num_demo_participants=50,
         use_browser_bots=True,
         expShortName='trunlot',
         expId=1616578277,
         treatment_list = ['FULL_BEST', 'BEST', 'BEST'],
         app_sequence=['truncated_reporting', 'quiz', 'payment']
      ),
   dict(
         name='SELF_EXPERIMENT',
         display_name="SELF_EXPERIMENT",
         num_demo_participants=50,
         use_browser_bots=False,
         expShortName='trunlot',
         expId=1616578277,
         treatment_list = ['FULL', 'FULL_BEST', 'BEST', 'TRUNCATED'],
         app_sequence=['truncated_reporting', 'quiz', 'payment']
      ),
    dict(
          name='BOT_EXPERIMENT',
          display_name="BOT_EXPERIMENT",
          num_demo_participants=50,
          use_browser_bots=True,
          expShortName='trunlot',
          expId=1616578277,
          treatment_list = ['FULL', 'FULL_BEST', 'BEST', 'TRUNCATED'],
          app_sequence=['truncated_reporting', 'quiz', 'payment']
       )

]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1/13, participation_fee=3, doc=""
)

ROOMS = [
    dict(
        name='DICELAB',
        display_name='DICELAB',
        #participant_label_file='dicelab_otree_labels.txt',
        #use_secure_urls=True
        )
]

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'EUR'
USE_POINTS = True
POINTS_CUSTOM_NAME = "Coins"

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = 'pkx&mvj6=ilo_dw$00!-9%%qtpenwv0wcnsj1+%^o7#0$ne9=)'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']
