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
from introduction.models import Constants as IntroConstants

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'payment'
    players_per_group = None
    num_rounds = 1
    base_pay = IntroConstants.base_pay



class Subsession(BaseSubsession):
    prolific_url = models.StringField()

    def creating_session(self):
        if "prolific_url" not in self.session.config:
            raise Exception("Prolific URL is missing. Add it to the session config.")
        self.prolific_url = self.session.config["prolific_url"]

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass
