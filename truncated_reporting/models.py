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

from itertools import cycle
import json
import random

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

    all_treatments = ['FULL', 'TRUNCATED', 'RANDOM', 'BEST']
    
    trunacted_text_lottery_1 = "The lottery pays with 10 % at least 90 Euro, 100 Euro is possible."


class Subsession(BaseSubsession):
    
    def creating_session(self):
        all_players = self.get_players()

        treatment_cycle = cycle(Constants.all_treatments)

        for p in all_players:
            # If the treatment is not specified in the session config,
            # we balance across the session
            player_treatment = self.session.config.get('treatment', next(treatment_cycle))
            assert player_treatment in Constants.all_treatments, "Unknown treatment indicator."
            p.treatment = player_treatment
            
            # Draw sample if needed
            if p.treatment in ['RANDOM', 'BEST']:
                p.draw_sample()

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    
    wtp_lottery_1 = models.CurrencyField(label="How much are you willing to pay to play this lottery?")
    treatment = models.StringField()
    all_draws = models.LongStringField()
    subsample = models.LongStringField()

    def set_all_draws(self, x):
        self.all_draws = json.dumps(x)

    def get_all_draws(self):
        return json.loads(self.all_draws)

    def set_subsample(self, x):
        self.subsample = json.dumps(x)

    def get_subsample(self):
        return json.loads(self.subsample)


    def draw_sample(self):
        """

        A method to draw a random sample from the lottery of which a subsample
        will be displayed to the participants.
        """
        total_sample = random.choices(population=list(Constants.lottery_1.keys()),
                                      weights=list(Constants.lottery_1.values()),
                                      k=Constants.sample_size)
        if self.treatment == 'BEST':
            subsample = sorted(total_sample, reverse=True)[:Constants.draws]
        elif self.treatment == 'RANDOM':
            subsample = random.sample(total_sample, Constants.draws)
        else:
            raise Exception(f'There is no sampeling in the treatment {self.treatment}.')

        self.set_all_draws(total_sample)
        self.set_subsample(subsample)