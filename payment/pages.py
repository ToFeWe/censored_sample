from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class YouFinished(Page):
    pass




class ToProlific(Page):
    pass


page_sequence = [YouFinished, ToProlific]
