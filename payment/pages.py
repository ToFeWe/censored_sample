from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Payoff(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        context = self.participant.vars['all_payoff_info']
        return context


page_sequence = [Payoff]
