from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Decision(Page):
    form_model = 'player'
    form_fields = ['wtp_lottery']

    def vars_for_template(self):
        trunc_text = Constants.all_lotteries[self.player.lottery]['trunc_text']

        context = {
            'trunc_text': trunc_text
        }
        
        if self.player.treatment in ['BEST', 'RANDOM']:
            extend_dict = {
                'subsample': self.player.get_subsample(),
                
            }
            context.update(extend_dict)

        elif self.player.treatment == 'FULL':
            current_lottery_dist = Constants.all_lotteries[self.player.lottery]['dist']
            probs_scaled = [int(p * 100) for p in current_lottery_dist.values()]
            payoffs = list(current_lottery_dist.keys())
            
            # To display the table correctly for changing number of payoffs
            colspan_table = len(payoffs)+1
            extend_dict ={
            'probs_scaled': probs_scaled,
            'payoffs': payoffs,
            'colspan_table': colspan_table
            }
            context.update(extend_dict)

        return context


page_sequence = [Decision]
