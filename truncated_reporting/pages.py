from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class Introduction(Page):
    def is_displayed(self):
        return self.round_number == 1

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
            probs_scaled = [int(round(p * 100)) for p in current_lottery_dist.values()]
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
