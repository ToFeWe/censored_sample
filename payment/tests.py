from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
from otree.api import Submission

class PlayerBot(Bot):
    def play_round(self):
        # If she fails the attention check she never arrives here
        if self.participant.vars.get('failed_attention', False) is False:
            if self.participant.vars['comprehension_passed'] is False:
                assert "You did not answer the comprehension questions" in self.html
            else:
                assert "You have completed this study in its entirety" in self.html
            yield pages.YouFinished
            yield Submission(pages.ToProlific, check_html=False)
