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
import random

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'introduction'
    players_per_group = None
    num_rounds = 1
    time_to_finish = 20 # Minutes
    base_pay =  4 # in Dollar
    n_lotteries = 5

    all_treatments = ['FULL', 'TRUNCATED', 'BEST', 'FULL_BEST']


class Subsession(BaseSubsession):
    def creating_session(self):
        all_players = self.get_players()

        # Determine treatment in the first round,
        # the paid lottery and the lottery order.
        # This info will be used below for each round.
        if self.round_number == 1:
            # If the treatment is not specified in the session config,
            # we balance across the session
            treatments_to_cycle = self.session.config.get('treatment_list', Constants.all_treatments.copy())

            # Random shuffle the list before creating the cycle 
            random.shuffle(treatments_to_cycle)
            print(treatments_to_cycle)

            # Create the cycle
            treatment_cycle = cycle(treatments_to_cycle)

            for p in all_players:
                # Treatment is determined
                p.participant.vars['treatment'] = next(treatment_cycle)
                p.treatment = p.participant.vars['treatment']

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    attention_check = models.StringField(label="")
    attention_check_num = models.IntegerField()
    failed_attention = models.BooleanField()

    prolific_id = models.StringField(label="Your Prolific-ID:")


    # We already assign treatments in this app
    treatment = models.StringField()

    # Comprehension questions

    comprehension_question_1 = models.IntegerField(label="", #1. Which payoffs are possible for the following lottery?
                                                  choices=[[1, "It is possible that I get paid both 30 coins and 80 coins, i.e., I may receive a total amount of 110 coins from this lottery."],
                                                           [2, "I receive EITHER 30 coins OR 80 coins OR 0 coins from this lottery."],
                                                           [3, "I will receive at least some money with certainty."]], 
                                                  widget=widgets.RadioSelect)

    comprehension_question_2 = models.IntegerField(label="", #2. What is the probability to get a payoff of 30 coins for the following lottery?
                                                  choices=[[1, "The probability to receive 30 coins is 60 %."],
                                                           [2, "The probability to receive 30 coins is 40 %."],
                                                           [3, "The probability to receive 30 coins is 0 %."]], 
                                                  widget=widgets.RadioSelect)
    comprehension_passed = models.BooleanField() 

    def validate_comprehension_questions(self):
        """ Validate if both comprehension questions have been answered correct. """
        both_correct =  (self.comprehension_question_1 == 2) & (self.comprehension_question_2 == 2)
        self.comprehension_passed = both_correct

        # Also write to participant variables as we have to access it in the next app
        # Note we only need to check the comprehension check in the next app and not
        # the attention check as the player would not arrive to the next app if he failed

        self.participant.vars['comprehension_passed'] = both_correct

    def get_general_instruction_vars(self):
        context = {
            'exchange_rate': int(1/self.session.config['real_world_currency_per_point']),
        }

        return context