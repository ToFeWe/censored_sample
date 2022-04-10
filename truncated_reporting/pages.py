from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from .models import sort_lottery, create_lottery

class Introduction(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return self.player.get_general_instruction_vars()

class Decision(Page):
    form_model = 'player'
    form_fields = ['wtp_lottery', 'belief_sequence', 'belief']

    def vars_for_template(self):
        context = dict()
        
        # Sort the lottery
        current_sorted_lottery = sort_lottery(
                                    create_lottery(
                                       q=self.player.mid_probability,
                                       x=self.player.max_payoff
                                       )
                                    )
        sorted_payoffs, sorted_probs = zip(*current_sorted_lottery)
        
        # Split
        payoff_low, payoff_mid, payoff_high = sorted_payoffs
        prob_low, prob_mid, prob_high = sorted_probs
        
        # For the treatments with censoring we calculate the joint values
        # directly here
        prob_upper_joint = prob_mid + prob_high

        # Add all variables to the context (quick and dirty)
        context['payoff_low'] = payoff_low
        context['payoff_mid'] = payoff_mid
        context['payoff_high'] = payoff_high

        # Scale also up and round due to floating points
        context['prob_low'] = int(round(prob_low * 100))
        context['prob_mid'] = int(round(prob_mid * 100))
        context['prob_high'] = int(round(prob_high * 100))

        context['prob_upper_joint'] = int(round(prob_upper_joint * 100))
        
        
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
                # self.player.save_payoff_info()

page_sequence = [Introduction, Decision]
