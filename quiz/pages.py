from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class General(Page):
    form_model = 'player'
    form_fields = ['q_age', 'q_gender', 'q_study_level', 'q_study_field',
                   'q_semester', 'q_n_experiment', 'q_similar_experiment',
                   'q_abitur', 'q_math', 'q_budget', 'q_spending']

class Falk(Page):
    form_model = 'player'
    form_fields = ['q_falk1']
    # , 'q_falk2',
    #                'q_falk3', 'q_falk4',
    #                'q_falk5', 'q_falk6']



page_sequence = [General, Falk]
