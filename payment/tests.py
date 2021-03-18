from otree.api import Currency as c, currency_range, expect, Submission
from . import pages
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):
    def play_round(self):
        # TODO Add tests
        yield Submission(pages.Payoff, check_html=False)
