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

author = 'Your name here'

doc = """
Your app description
"""

def make_full_text(lottery):
    # TODO: Add doc
    dict_items_sorted = sorted(lottery.items(), key=lambda x:x[0]) # TODO: Should be default behavior?
    dict_items_sorted_recaled = [(value, int(round(prob * 100))) for value, prob in dict_items_sorted]
    if len(dict_items_sorted) != 3:
        raise Exception("Only works for three part lotteries")
    else:
        out_string = (f"Die Auszahlung der Lotterie beträgt {dict_items_sorted_recaled[0][0]}, {dict_items_sorted_recaled[1][0]} oder {dict_items_sorted_recaled[2][0]} Taler. "
                      f"Die Lotterie zahlt mit einer Wahrscheinlichkeit von {dict_items_sorted_recaled[0][1]}% genau {dict_items_sorted_recaled[0][0]} Taler, "
                      f"mit {dict_items_sorted_recaled[1][1]}% genau {dict_items_sorted_recaled[1][0]}"
                      f" Taler und mit {dict_items_sorted_recaled[2][1]}% genau {dict_items_sorted_recaled[2][0]} Taler.")

        return out_string
def make_trunc_text(lottery):
    """
    A function to create a text that is displayed for
    the given *lottery* in the truncated form

    Args:
        lottery (dict): Value: Payoff of the lottery
                        Key: Probabilities

    Returns:
        String: Truncated description of the lottery
    """
    dict_items_sorted = sorted(lottery.items(), key=lambda x:x[0]) # TODO: Should be default behavior?
    if len(dict_items_sorted) != 3:
        raise Exception("Only works for three part lotteries")
    else:
        two_last_probs = dict_items_sorted[-1][1] + dict_items_sorted[-2][1]
        accumulate_last_probs= int(round(two_last_probs * 100))

        out_string = (f"Die Auszahlung der Lotterie beträgt {dict_items_sorted[0][0]}, {dict_items_sorted[1][0]} oder {dict_items_sorted[2][0]} Taler. "
                      f"Die Wahrscheinlichkeit mindestens {dict_items_sorted[1][0]} Taler zu bekommen beträgt {accumulate_last_probs} %.")
        return out_string

class Constants(BaseConstants):
    name_in_url = 'truncated_reporting'
    players_per_group = None

    all_lotteries = {
        'lottery_1' : { 
            'dist': {
                0: 0.9,
                90: 0.09,
                100: 0.01,
            }
        },
        'lottery_2': {  
            'dist': {
                0: 0.8,
                80: 0.19,
                100: 0.01,
            }
        },
        'lottery_3': { 
            'dist': {
                0: 0.7,
                70: 0.29,
                100: 0.01,
            }
        },
        'lottery_4': { 
            'dist': {
                0: 0.6,
                60: 0.39,
                100: 0.01,
            }
        },
        'lottery_5': { 
            'dist': {
                0: 0.5,
                50: 0.49,
                100: 0.01,
            }
        },
        'lottery_6': { 
            'dist': {
                0: 0.9,
                90: 0.09,
                110: 0.01,
            },
        },
        'lottery_7': { 
            'dist': {
                0: 0.8,
                90: 0.19,
                110: 0.01,
            }
        },
        'lottery_8': { 
            'dist': {
                0: 0.7,
                90: 0.29,
                120: 0.01,
            }
        },
        'lottery_9': { 
            'dist': {
                0: 0.6,
                90: 0.39,
                130: 0.01,
            }
        },
        'lottery_10': { 
            'dist': {
                0: 0.5,
                90: 0.49,
                140: 0.01,
            }
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
            if self.round_number == 1:
                # Create random lottery order for each participant
                p.participant.vars['lottery_order'] = random.sample(
                    list(
                        Constants.all_lotteries.keys()
                    ),
                    len(Constants.all_lotteries)
                )
                # Draw which round/lottery is paid
                # Note: randint fully inclusive with bounds
                p.participant.vars['paid_lottery_round'] = random.randint(1,Constants.num_rounds)

            # Write lottery to database
            p.lottery = p.participant.vars['lottery_order'][self.round_number-1]
            
            # Write paid round/lottery to database for each round
            p.paid_lottery_round = p.participant.vars['paid_lottery_round']

            # Determine random price for lottery
            # Note randint is inclusive for upper and lower bound
            ub_price = max(Constants.all_lotteries[p.lottery]['dist'].keys())
            p.price_lottery = random.randint(0, ub_price)

            player_treatment = next(treatment_cycle)
            assert player_treatment in Constants.all_treatments, "Unknown treatment indicator."
            p.treatment = player_treatment
            
            # Draw sample if needed
            if p.treatment in ['RANDOM', 'BEST']:
                p.draw_sample()

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    
    # Some attention/Comprehension checks
    conversion_check = models.IntegerField(label=('Nehmen Sie an, dass Ihre zusätzliche Auszahlung 75 Taler beträgt.'
                                                  ' Wie viel ist das umgerechnet in Euro?'))
    
    # Example lottery: 50% 0 Taler, 30% 50 Taler, 20 % 60 Taler
    example_1_check = models.StringField(label=('Nehmen Sie an, die Lotterie zahlt mit einer Wahrscheinlichkeit von 50% genau 0 Taler, mit 30% genau 50 Taler und mit 20% genau 60 Taler. '
                                                'Wie wird der tatsächliche Preis für die Lotterie bestimmt?'),
                                         choices=['Der Preis wird zufällig ausgewählt und kann zwischen 0 und 60 Talern liegen.',
                                                  'Der Preis wird zufällig ausgewählt und kann zwischen 10 und 50 Talern liegen.',
                                                  'Der Preis liegt immer bei 22 Talern.'])

    example_2_check = models.StringField(label=('Nehmen Sie folgende Situation an: Sie geben an, dass Sie bereit sind 24 Taler zu zahlen, um eine '
                                                'Lotterie zu spielen. Der Preis der Lotterie liegt bei 20 Talern. Wie wird ihre zusätzliche Auszahlung bestimmt?'),
                                         choices=['Die zusätzliche Auszahlung entspricht in diesem Fall dem Preis der Lotterie.',
                                                  'Die zusätzliche Auszahlung wird durch einen Zufallszug aus der Lotterie bestimmt.'])


    lottery = models.StringField()
    wtp_lottery = models.CurrencyField(label="", min=0)
    price_lottery = models.CurrencyField()
    paid_lottery_round = models.IntegerField() # Indicator which lottery round is paid
    lottery_played = models.BooleanField() # True if the payoff was deterimned by lottery

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
            self.lottery_played = False
        else:
            # Else she plays the lottery
            relevant_lottery_dist = Constants.all_lotteries[player_in_paid_round.lottery]['dist']
            self.payoff = random.choices(population=list(relevant_lottery_dist.keys()),
                                         weights=list(relevant_lottery_dist.values()),
                                         k=1)[0]
            self.lottery_played = True

    def save_payoff_info(self):
        """
        
        Helper function to save the relevant payment information to
        participant dict for the payment app to retrieve it.
        """

        player_in_paid_round = self.in_round(self.paid_lottery_round)
        
        # Info on the lottery show
        paid_lottery_dist = Constants.all_lotteries[player_in_paid_round.lottery]['dist']
        probs_scaled = [int(round(p * 100)) for p in paid_lottery_dist.values()]
        payoffs = list(paid_lottery_dist.keys())
        
        # To display the table correctly for changing number of payoffs
        colspan_table = len(payoffs)+1

        # Some info on the relevant decision from the participant
        relevant_wtp = player_in_paid_round.wtp_lottery
        relevant_price = player_in_paid_round.price_lottery

        all_payoff_info ={
            'probs_scaled': probs_scaled,
            'payoffs': payoffs,
            'participant_payoff': self.participant.payoff,
            'colspan_table': colspan_table,
            'paid_lottery_round': self.paid_lottery_round,
            'relevant_wtp': relevant_wtp,
            'lottery_played': self.lottery_played,
            'relevant_price': relevant_price,
            'additional_money': self.payoff.to_real_world_currency(self.session),
            'show_up': self.session.config['participation_fee'],
            'total_money': self.participant.payoff_plus_participation_fee()
        }
        self.participant.vars['all_payoff_info'] = all_payoff_info