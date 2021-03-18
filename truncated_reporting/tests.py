from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):
    def play_round(self):
        if self.round_number == 1:
            yield pages.Introduction
            yield pages.RogerThat, dict(conversion_check=5,
                                        example_1_check='Der Preis wird zufällig ausgewählt und kann zwischen 0 und 60 Talern liegen.',
                                        example_2_check='Die zusätzliche Auszahlung wird durch einen Zufallszug aus der Lotterie bestimmt.')
        yield pages.Decision, dict(wtp_lottery=50)            
