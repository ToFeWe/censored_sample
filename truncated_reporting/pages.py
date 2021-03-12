from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from .models import make_trunc_text, make_full_text

class Introduction(Page):
    def is_displayed(self):
        return self.round_number == 1

class Decision(Page):
    form_model = 'player'
    form_fields = ['wtp_lottery']

    def vars_for_template(self):
        context = {
        
        }
        
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
        if self.round_number == Constants.num_rounds:
            self.player.calc_payoff()

class Payoff(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
            player_in_paid_round = self.player.in_round(self.player.paid_lottery)
            
            # Info on the lottery show
            paid_lottery_dist = Constants.all_lotteries[player_in_paid_round.lottery]['dist']
            probs_scaled = [int(round(p * 100)) for p in paid_lottery_dist.values()]
            payoffs = list(paid_lottery_dist.keys())
            
            # To display the table correctly for changing number of payoffs
            colspan_table = len(payoffs)+1

            # Some info on the relevant decision from the participant
            relevant_wtp = player_in_paid_round.wtp_lottery
            relevant_price = player_in_paid_round.price_lottery

            context ={
                'probs_scaled': probs_scaled,
                'payoffs': payoffs,
                'colspan_table': colspan_table,
                'paid_lottery_round': self.player.paid_lottery,
                'relevant_wtp': relevant_wtp,
                'relevant_price': relevant_price,
                'additional_money': self.player.payoff.to_real_world_currency(self.session),
                'show_up': self.session.config['participation_fee'],
                'total_money': self.participant.payoff_plus_participation_fee()
            }
            return context

page_sequence = [Introduction, Decision, Payoff]
