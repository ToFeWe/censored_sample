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

    all_lotteries = {
        'lottery_1' : { 
            'dist': {
                0: 0.9,
                90: 0.09,
                100: 0.01,
            },
            'trunc_text': "The lottery pays with 10 % at least 90 Euro, 100 Euro is possible."
        },
        'lottery_2': { 
            'dist': {
                0: 0.8,
                80: 0.19,
                100: 0.01,
            },
            'trunc_text': "The lottery pays with 20 % at least 80 Euro, 100 Euro is possible."
        },
        'lottery_3': { 
            'dist': {
                50: 0.5,
                100: 0.5
            },
            'trunc_text': "The lottery pays with 50 % at least 50 Euro, 100 Euro is possible."
        }

    }

    num_rounds = len(all_lotteries)


    sample_size = 250
    draws = 5

    all_treatments = ['FULL', 'TRUNCATED', 'RANDOM', 'BEST']
    

class Subsession(BaseSubsession):
    
    def creating_session(self):
        all_players = self.get_players()

        treatment_cycle = cycle(Constants.all_treatments)

        for p in all_players:
            # Create random lottery order for each participant
            if self.round_number == 1:
                p.participant.vars['lottery_order'] = random.sample(
                    list(
                        Constants.all_lotteries.keys()
                    ),
                    len(Constants.all_lotteries)
                )
            # Write lottery to database
            p.lottery = p.participant.vars['lottery_order'][self.round_number-1]

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
    
    lottery = models.StringField()
    wtp_lottery = models.CurrencyField(label="How much are you willing to pay to play this lottery?")
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
        current_lottery_dist = Constants.all_lotteries[self.lottery]['dist']
        total_sample = random.choices(population=list(current_lottery_dist.keys()),
                                      weights=list(current_lottery_dist.values()),
                                      k=Constants.sample_size)
        if self.treatment == 'BEST':
            subsample = sorted(total_sample, reverse=True)[:Constants.draws]
        elif self.treatment == 'RANDOM':
            subsample = random.sample(total_sample, Constants.draws)
        else:
            raise Exception(f'There is no sampeling in the treatment {self.treatment}.')

        self.set_all_draws(total_sample)
        self.set_subsample(subsample)