from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class OrseeID(Page):
    form_model = 'player'
    form_fields = ['orsee_id']

    def is_displayed(self):
        # Page is only required if we did not use
        # the link to pass the orsee id via the 
        # participant label.
        if self.participant.label is None:
            return True
        else:
            self.player.orsee_id = self.participant.label

    def before_next_page(self):
        self.participant.label = self.player.orsee_id

class Payoff(Page):
    def vars_for_template(self):
        context = self.participant.vars['all_payoff_info']

        paymentURL = self.player.create_paymentURL()
        context.update(dict(paymentURL = paymentURL))
        return context
            

page_sequence = [OrseeID, Payoff]
