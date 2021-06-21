from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from .models import make_trunc_text, make_full_text, get_highest_payoff_state

class Introduction(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return self.player.get_general_instruction_vars()

class Decision(Page):
    form_model = 'player'
    form_fields = ['wtp_lottery']

    def vars_for_template(self):
        context = dict()
        
        if self.player.treatment in ['FULL', 'FULL_BEST']:
            lottery_text = make_full_text(Constants.all_lotteries[self.player.lottery]['dist'])
        else:
            lottery_text = make_trunc_text(Constants.all_lotteries[self.player.lottery]['dist'])
        
        context['lottery_text'] = lottery_text
        
        
        if self.player.treatment in ['BEST', 'FULL_BEST', 'RANDOM']:
            extend_dict = {
                'subsample': self.player.get_subsample(),
                
            }
            context.update(extend_dict)
            
        # get other variables for instructions
        context.update(self.player.get_general_instruction_vars())
        return context

    def before_next_page(self):
        # In the last round calculate payoffs
        # and save all info about payment
        # to participant dict
        if self.round_number == Constants.num_rounds:
            # In best and truncated we do this after the belief page
            if self.player.treatment not in ['BEST', 'TRUNCATED']:
                self.player.calc_payoff()
                self.player.save_payoff_info()


class Belief(Page):
    form_model = 'player'
    form_fields = ['belief', 'belief_sequence']

    def vars_for_template(self):
        context = dict()
        
        if self.player.treatment == "FULL":
            lottery_text = make_full_text(Constants.all_lotteries[self.player.lottery_for_belief]['dist'])
        else:
            lottery_text = make_trunc_text(Constants.all_lotteries[self.player.lottery_for_belief]['dist'])
        
        context['lottery_text'] = lottery_text
        
        
        if self.player.treatment in ['BEST', 'RANDOM']:
            # Retrieve the sample he has seen in the first round
            player_in_first_round = self.player.in_round(1)
            extend_dict = {
                'subsample': player_in_first_round.get_subsample(),
                
            }
            context.update(extend_dict)
            
        # get other variables for instructions
        context.update(self.player.get_general_instruction_vars())

        # Get the highest payoff state for the given lottery
        highest_payoff_state = get_highest_payoff_state(Constants.all_lotteries[
                                                                    self.player.lottery_for_belief
                                                                ]['dist'])
        # GEt the highest possible prior a participant could report
        max_value_slider = self.player.slider_max()

        # Add both to context
        context.update({
            'highest_payoff_state': highest_payoff_state,
            'max_value_slider': max_value_slider
        })

        return context

    def is_displayed(self):
        # Only shown in the last round and only if the probabilities have been censored
        return ((self.round_number == Constants.num_rounds) and self.player.treatment in ['BEST','TRUNCATED'])


    def before_next_page(self):
        self.player.calc_belief_bonus()
        # We need to calculate the final payoff. We have not done this on the page before
        # for treatments in which we elicit beliefs
        self.player.calc_payoff()
        self.player.save_payoff_info()

page_sequence = [Introduction, Decision, Belief]
