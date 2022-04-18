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

    all_treatments = ['FULL', 'TRUNCATED', 'BEST', 'FULL_BEST']
    
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
            if p.treatment in ['BEST', 'FULL_BEST']:
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


    # Belief that is reported for each lottery for the 
    # highest payoff state.
    belief = models.IntegerField(label="")
    belief_sequence = models.LongStringField(blank=True)
    belief_bonus_won = models.BooleanField()

    # Also save the probability to win the belief bonus.
    # Note that this is mostly for debugging purposes
    win_probability = models.FloatField()

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
        if self.treatment in ['BEST', 'FULL_BEST']:
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

        # TODO: Adjust the whole belief stuff to the new logic
        # Belief Bonus if in relevant treatment has to be added
        # Note that this belief bonus was calculated in the same round.
        # if self.treatment in ['TRUNCATED', 'BEST']:
        #     if self.belief_bonus_won:
        #         self.payoff += c(Constants.belief_bonus)

    # TODO: I guess I do not need this anymore given that
    # we pay people ex-post?!
    # def save_payoff_info(self):
    #     """
        
    #     Helper function to save the relevant payment information to
    #     participant dict for the payment app to retrieve it.
    #     """

    #     player_in_paid_round = self.in_round(self.paid_lottery_round)
        
    #     # Info on the lottery show
    #     paid_lottery_dist = Constants.all_lotteries[player_in_paid_round.lottery]['dist']
    #     probs_scaled = [int(round(p * 100)) for p in paid_lottery_dist.values()]
    #     payoffs = list(paid_lottery_dist.keys())
        
    #     # To display the table correctly for changing number of payoffs
    #     colspan_table = len(payoffs)+1

    #     # Some info on the relevant decision from the participant
    #     relevant_wtp = player_in_paid_round.wtp_lottery
    #     relevant_price = player_in_paid_round.price_lottery

    #     all_payoff_info ={
    #         'probs_scaled': probs_scaled,
    #         'payoffs': payoffs,
    #         'participant_payoff': self.participant.payoff,
    #         'colspan_table': colspan_table,
    #         'paid_lottery_round': self.paid_lottery_round,
    #         'relevant_wtp': relevant_wtp,
    #         'lottery_played': self.lottery_played,
    #         'lottery_payment': self.lottery_payment,
    #         'relevant_price': relevant_price,
    #         'additional_money': self.payoff.to_real_world_currency(self.session),
    #         'show_up': self.session.config['participation_fee'],
    #         'total_money': self.participant.payoff_plus_participation_fee(),
    #         'exchange_rate': int(1/self.session.config['real_world_currency_per_point']),
    #         'treatment': self.treatment,
    #         'win_probability': self.win_probability
    #     }
    #     # Add belief bonus from current round if needed
    #     if self.treatment in ['BEST', 'TRUNCATED']:
    #         all_payoff_info.update({'belief_bonus_taler': self.belief_bonus_won * Constants.belief_bonus })


    #     self.participant.vars['all_payoff_info'] = all_payoff_info

    def get_general_instruction_vars(self):
        context = {
            'exchange_rate': int(1/self.session.config['real_world_currency_per_point']),
            'show_up': self.session.config['participation_fee']
        }

        return context

    # TODO: Rework
    def calc_belief_bonus(self):
        """

        Calculate the belief bonus given the BSR.
        """
        relevant_lottery = Constants.all_lotteries[self.lottery_for_belief]['dist']
        sorted_lottery = sort_lottery(relevant_lottery)

        probability_highest_state_scaled_up = sorted_lottery[-1][1] * 100
        probability_lowest_state = sorted_lottery[0][1]

        max_prob_can_report_scaled_up = int(round((1 - probability_lowest_state) * 100))
        self.win_probability = 1 - abs((self.belief - probability_highest_state_scaled_up) / max_prob_can_report_scaled_up)
        self.belief_bonus_won = np.random.choice([True, False], p=[self.win_probability, 1-self.win_probability])
