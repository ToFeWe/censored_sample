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

from itertools import accumulate, cycle
import json
import random
import math
import numpy as np
import warnings

author = 'Your name here'

doc = """
Your app description
"""

def create_lottery(q, x):
    """
    
    Create the lottery that is played in the current round. Note that the lottery
    always has the following structure:
    L =(0 coins, 100- q - 1% ;
        10 coins, q % ;
        x coins, 1%)
    
    where *q* is the probability for the middle payoff state and x is the highest 
    payoff state
    """
    lottery = {
        0: 1 - q - 0.01,
        10: q,
        x: 0.01
    }
    return lottery

# TODO: Moves those functions to separate utils file
def sort_lottery(lottery):
    """
    
    Sorts a lottery by payoff state in an increasing order.

    Args:
        lottery (dict): Lottery that is being used.
    """
    dict_items_sorted = sorted(lottery.items(), key=lambda x:x[0])
    return dict_items_sorted

class Constants(BaseConstants):
    name_in_url = 'trunlot_experiment'
    players_per_group = None
    
    max_payoff_states = [100, 120, 140, 160, 180]
    mid_probabilites = [0.09, 0.19, 0.29, 0.39, 0.49]

    num_rounds = 5

    sample_size = 400
    draws = 5

    last_n_draws = 50

    all_treatments = ['FULL', 'BEST', 'BEST_NUDGE']
    belief_bonus = 13

class Subsession(BaseSubsession):
    
    def creating_session(self):
        all_players = self.get_players()

        # Determine the lotteries.
        # This info will be used below for each round.
        if self.round_number == 1:

            for p in all_players:
                # Create random shuffles of payoff states...
                max_payoff_states_shuffled = Constants.max_payoff_states.copy()
                random.shuffle(max_payoff_states_shuffled)
                # .. and probabilities.
                mid_probabilites_shuffled = Constants.mid_probabilites.copy()
                random.shuffle(mid_probabilites_shuffled)

                # Zip them together to get pairs and save it to participants
                # variables.
                p.participant.vars['payoff_probability_combinations'] = list(zip(max_payoff_states_shuffled,
                                                                                 mid_probabilites_shuffled))

                # Draw which round/lottery is paid
                # Note: randint fully inclusive with bounds
                p.participant.vars['paid_lottery_round'] = random.randint(1,Constants.num_rounds)

        # Write all info to the database for each round
        for p in all_players:
            # Write the current lottery values to database
            p.max_payoff, p.mid_probability = p.participant.vars['payoff_probability_combinations'][self.round_number-1]
            
            # Write paid round/lottery to database for each round
            p.paid_lottery_round = p.participant.vars['paid_lottery_round']

            # Determine random price for lottery
            # Note randint is inclusive for upper and lower bound
            p.price_lottery = random.randint(0, p.max_payoff)


            # Write treatment to database for each round
            # Note that the treatment has been assigned in the introduction 
            # app.
            if 'treatment' not in p.participant.vars:
                if p.round_number == 1:
                    warnings.warn('The treatment variable has not been assigned.'
                                'Defaults to random treatment')
                    p.participant.vars['treatment'] = random.choice(Constants.all_treatments)
                    p.treatment = p.participant.vars['treatment']
                else:
                    p.treatment = p.participant.vars['treatment']
            else:
                p.treatment = p.participant.vars['treatment']
                assert p.treatment in Constants.all_treatments, "Unknown treatment indicator."

            # Draw sample if needed
            if p.treatment in ['BEST', 'BEST_NUDGE', 'BEST_INFO']:
                p.draw_sample()


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    # Two variables define the lottery in the given period
    max_payoff = models.IntegerField()
    mid_probability = models.FloatField()

    wtp_lottery = models.CurrencyField(label="", min=0)
    price_lottery = models.CurrencyField()
    paid_lottery_round = models.IntegerField() # Indicator which lottery round is paid
    lottery_played = models.BooleanField() # True if the payoff was determined by lottery

    # Fields to save the amount earn from the lottery potential lottery
    # draw. Note that this field is zero if the lottery was not played
    # as the price is the payoff in this case.
    lottery_payment = models.CurrencyField()


    treatment = models.StringField()
    all_draws = models.LongStringField()
    subsample = models.LongStringField()


    # Lottery variables for the nudge treatment
    x_mid_draws = models.IntegerField()
    y_high_draws = models.IntegerField()

    # Belief that is reported for each lottery for the 
    # highest payoff state.
    belief = models.IntegerField(label="")
    belief_sequence = models.LongStringField(blank=True)

    def wtp_lottery_max(self):
        """ 
        Helper function to determine the maximum for the given 
        round dynamically as it differs by lottery."""
        
        return self.max_payoff

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
        current_lottery_dist = create_lottery(q=self.mid_probability,
                                              x=self.max_payoff)
        total_sample = random.choices(population=list(current_lottery_dist.keys()),
                                      weights=list(current_lottery_dist.values()),
                                      k=Constants.sample_size)

        # If we consider a policy treatment, we also check for the
        # last draws of the sample     
        if self.treatment in ['BEST_NUDGE', 'BEST_INFO']:
            last_draws = total_sample[-Constants.last_n_draws:]
            self.x_mid_draws = last_draws.count(10) # mid payoff is always ten!
            self.y_high_draws = last_draws.count(self.max_payoff)
        
        if self.treatment in ['BEST', 'BEST_NUDGE', 'BEST_INFO']:
            subsample = sorted(total_sample, reverse=True)[:Constants.draws]
        else:
            raise Exception(f'There is no sampling in the treatment {self.treatment}.')

        self.set_all_draws(total_sample)
        self.set_subsample(subsample)
    
    def calc_payoff(self):
        """

        Helper function to determine final payoff.
        """
        player_in_paid_round = self.in_round(self.paid_lottery_round)
        relevant_wtp_player = player_in_paid_round.wtp_lottery
        relevant_price =  player_in_paid_round.price_lottery
        
        # If the wtp is below the price, the player
        # receives the price
        if relevant_price>relevant_wtp_player:
            self.payoff = relevant_price
            self.lottery_payment = 0 #  No lottery payment in this case
            self.lottery_played = False
        else:
            # Else she plays the lottery
            relevant_lottery_dist = create_lottery(q=player_in_paid_round.mid_probability,
                                                   x=player_in_paid_round.max_payoff)
            self.lottery_payment = random.choices(population=list(relevant_lottery_dist.keys()),
                                                  weights=list(relevant_lottery_dist.values()),
                                                  k=1)[0]
            self.payoff = self.lottery_payment
            self.lottery_played = True


    def get_general_instruction_vars(self):
        context = {
            'exchange_rate': int(1/self.session.config['real_world_currency_per_point']),
            'show_up': self.session.config['participation_fee']
        }

        return context
