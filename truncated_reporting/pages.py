from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Decision(Page):
    form_model = 'player'
    form_fields = ['wtp_lottery_1']

    def vars_for_template(self):
        
        if self.player.treatment in ['BEST', 'RANDOM']:
            return {
                'subsample': self.player.get_subsample(),
                
            }
        elif self.player.treatment == 'FULL':
            probs_scaled = [int(p * 100) for p in Constants.lottery_1.values()]
            payoffs = list(Constants.lottery_1.keys())
            lottery_item = zip(payoffs, probs_scaled)

            return {
            'probs_scaled': probs_scaled,
            'payoffs': payoffs
            }


page_sequence = [Decision]
