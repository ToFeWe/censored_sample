from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from otree.api import Submission
from .models import Constants


class PlayerBot(Bot):
    cases = ['all_good'] # 'failed_attention', 'failed_comprehension', 
    def play_round(self):
        if self.case == 'failed_attention':
            some_string = ("This string has in total 14 words and "
                           "thus the check should fail please")
            yield pages.AttentionCheck, dict(attention_check=some_string)
            yield Submission(pages.AttentionCheckFail, check_html=False)
        else:
            some_longer_string = ("This string has in total 15 words and "
                                  "thus the check should not fail please")
            yield pages.AttentionCheck, dict(attention_check=some_longer_string)
            yield pages.Welcome, dict(prolific_id="Some-ID")
            yield pages.Instructions_1
            yield pages.Instructions_2
            yield pages.Instructions_3
            yield pages.PaymentInstructions
            
            if self.case == 'failed_comprehension':
                yield pages.Comprehension, dict(comprehension_question_1=1,
                                                comprehension_question_2=3)
                yield pages.ComprehensionFail
            else:
                # All good case
                yield pages.Comprehension, dict(comprehension_question_1=2,
                                                comprehension_question_2=2)
                yield pages.StartExperiment

