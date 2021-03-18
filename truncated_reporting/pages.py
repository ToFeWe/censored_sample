from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from .models import make_trunc_text, make_full_text

class Introduction(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'show_up': self.session.config['participation_fee']
        }

class RogerThat(Page):
    form_model = 'player'
    form_fields = ['conversion_check',
                   'example_1_check',
                   'example_2_check']


    def is_displayed(self):
        return self.round_number == 1


class Decision(Page):
    form_model = 'player'
    form_fields = ['wtp_lottery']

    def vars_for_template(self):
        context = dict()
        
        if self.player.treatment == "FULL":
            lottery_text = make_full_text(Constants.all_lotteries[self.player.lottery]['dist'])
        else:
            lottery_text = make_trunc_text(Constants.all_lotteries[self.player.lottery]['dist'])
        
        context['lottery_text'] = lottery_text
        
        
        if self.player.treatment in ['BEST', 'RANDOM']:
            extend_dict = {
                'subsample': self.player.get_subsample(),
                
            }
            context.update(extend_dict)

        return context

    def before_next_page(self):
        # In the last round calculate payoffs
        # and save all info about payment
        # to participant dict
        if self.round_number == Constants.num_rounds:
            self.player.calc_payoff()
            self.player.save_payoff_info()


page_sequence = [Introduction, RogerThat, Decision]
