from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):
    def play_round(self):
        yield pages.General, dict(q_age=28,
                                  q_gender='Männlich',
                                  q_study_level='Masterabschluss',
                                  q_study_field='YOLO studies',
                                  q_semester=12,
                                  q_n_experiment=12,
                                  q_similar_experiment='Ja.',
                                  q_abitur=1,
                                  q_math=1,
                                  q_budget=10,
                                  q_spending=10)
        yield pages.Falk, dict(q_falk_risk=1,
                               q_falk_time=0,
                               q_falk_trust=10,
                               q_falk_neg_rec=6,
                               q_falk_pos_rec=3,
                               q_falk_altruism=500)