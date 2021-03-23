from otree.api import Currency as c, currency_range, expect, Submission
from . import pages
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):
    def play_round(self):
        yield pages.OrseeID, dict(orsee_id="lollo")
        

        price = self.participant.vars['all_payoff_info']['relevant_price']
        wtp = self.participant.vars['all_payoff_info']['relevant_wtp']
        if price < wtp:
            expect("Da der Preis kleiner oder", "in", self.html)
        else:
            expect("Da der Preis größer als Ihr Maximalpreis ist", "in", self.html)


        expect(str(self.participant.payoff_plus_participation_fee()), "in", self.html)
        yield Submission(pages.Payoff, check_html=False)
