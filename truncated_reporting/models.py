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

    # TODO: Make function for trunc_text?
    all_lotteries = {
        'lottery_1' : { 
            'dist': {
                0: 0.9,
                90: 0.09,
                100: 0.01,
            },
            'trunc_text': "Die Auszahlung der Lotterie beträgt 0, 90 oder 100 Taler. Die Wahrscheinlichkeit mindestens 90 Taler zu bekommen beträgt 10%."
        },
        'lottery_2': {  
            'dist': {
                0: 0.8,
                80: 0.19,
                100: 0.01,
            },
            'trunc_text': "Die Auszahlung der Lotterie beträgt 0, 80 oder 100 Taler. Die Wahrscheinlichkeit mindestens 80 Taler zu bekommen beträgt 20%."
        },
        'lottery_3': { 
            'dist': {
                0: 0.7,
                70: 0.29,
                100: 0.01,
            },
            'trunc_text': "Die Auszahlung der Lotterie beträgt 0, 70 oder 100 Taler. Die Wahrscheinlichkeit mindestens 70 Taler zu bekommen beträgt 20%."
        },
        'lottery_4': { 
            'dist': {
                0: 0.6,
                60: 0.39,
                100: 0.01,
            },
            'trunc_text': "Die Auszahlung der Lotterie beträgt 0, 60 oder 100 Taler. Die Wahrscheinlichkeit mindestens 60 Taler zu bekommen beträgt 20%."
        },
        'lottery_5': { 
            'dist': {
                0: 0.5,
                50: 0.49,
                100: 0.01,
            },
            'trunc_text': "Die Auszahlung der Lotterie beträgt 0, 50 oder 100 Taler. Die Wahrscheinlichkeit mindestens 50 Taler zu bekommen beträgt 20%."
        },
        'lottery_6': { 
            'dist': {
                0: 0.9,
                90: 0.09,
                110: 0.01,
            },
            'trunc_text': "Die Auszahlung der Lotterie beträgt 0, 90 oder 110 Taler. Die Wahrscheinlichkeit mindestens 90 Taler zu bekommen beträgt 10%."
        },
        'lottery_7': { 
            'dist': {
                0: 0.8,
                90: 0.19,
                110: 0.01,
            },
            'trunc_text': "Die Auszahlung der Lotterie beträgt 0, 90 oder 110 Taler. Die Wahrscheinlichkeit mindestens 90 Taler zu bekommen beträgt 20%."
        },
        'lottery_8': { 
            'dist': {
                0: 0.7,
                90: 0.29,
                120: 0.01,
            },
            'trunc_text': "Die Auszahlung der Lotterie beträgt 0, 90 oder 120 Taler. Die Wahrscheinlichkeit mindestens 90 Taler zu bekommen beträgt 30%."
        },
        'lottery_9': { 
            'dist': {
                0: 0.6,
                90: 0.39,
                130: 0.01,
            },
            'trunc_text': "Die Auszahlung der Lotterie beträgt 0, 90 oder 130 Taler. Die Wahrscheinlichkeit mindestens 90 Taler zu bekommen beträgt 40%."
        },
        'lottery_10': { 
            'dist': {
                0: 0.5,
                90: 0.49,
                140: 0.01,
            },
            'trunc_text': "Die Auszahlung der Lotterie beträgt 0, 90 oder 140 Taler. Die Wahrscheinlichkeit mindestens 90 Taler zu bekommen beträgt 50%."
        }

    }

    num_rounds = len(all_lotteries)


    sample_size = 250
    draws = 5

    all_treatments = ['FULL', 'TRUNCATED', 'RANDOM', 'BEST']
    
class Subsession(BaseSubsession):
    
    def creating_session(self):
        all_players = self.get_players()

        # If the treatment is not specified in the session config,
        # we balance across the session
        treatments_to_cycle = self.session.config.get('treatment_list', Constants.all_treatments)
        treatment_cycle = cycle(treatments_to_cycle)

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

            player_treatment = next(treatment_cycle)
            assert player_treatment in Constants.all_treatments, "Unknown treatment indicator."
            p.treatment = player_treatment
            
            # Draw sample if needed
            if p.treatment in ['RANDOM', 'BEST']:
                p.draw_sample()

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    
    lottery = models.StringField()
    wtp_lottery = models.CurrencyField(label="", min=0)
    treatment = models.StringField()
    all_draws = models.LongStringField()
    subsample = models.LongStringField()


    def wtp_lottery_max(self):
        """ 
        Helper function to determine the maximum for the given 
        round dynamically as it differs by lottery."""
        
        all_payoffs=  list(Constants.all_lotteries[self.lottery]['dist'].keys())
        return max(all_payoffs)

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