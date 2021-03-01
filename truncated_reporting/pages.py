from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class MyPage(Page):
    def vars_for_template(self):
        return dict(ball_colors=['red'] * 36 + ['blue'] * 37) # etc


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [MyPage, ResultsWaitPage, Results]
