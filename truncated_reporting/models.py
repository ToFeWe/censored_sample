from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'truncated_reporting'
    players_per_group = None
    num_rounds = 1
    lottery_1 = {
        0: 0.9,
        90: 0.09,
        100: 0.01,
    }

    sample_size = 250
    draws = 5
    

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass
