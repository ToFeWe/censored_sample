from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class OrseeID(Page):
    form_model = 'player'
    form_fields = ['orsee_id']

    def before_next_page(self):
        # Save orsee id to participant dict for the admin
        # page.
        self.participant.vars['orsee_id'] = self.player.orsee_id

class Payoff(Page):
    def vars_for_template(self):
        context = self.participant.vars['all_payoff_info']
        return context


page_sequence = [OrseeID, Payoff]
