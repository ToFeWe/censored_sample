from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from otree.common import participant_start_url

class Payoff(Page):
    def vars_for_template(self):
        context = self.participant.vars['all_payoff_info']

        context.update(dict(payoff_link = "google.com"))
        return context
            

page_sequence = [Payoff]
