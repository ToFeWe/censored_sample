from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class General(Page):
    form_model = 'player'
    form_fields = ['q_age', 'q_gender', 'q_study_level', 'q_study_field',
                   'q_budget']

class Video_1(Page):
    form_model = 'player'
    form_fields = ['q_videogame_time', 'q_loot_box_what']

class Video_2(Page):
    form_model = 'player'
    form_fields = ["q_loot_box_spending", "q_loot_box_more_than_planned"]

    def is_displayed(self):
        # Only show if the person knows what a loot box is
        return self.player.q_loot_box_what == True

class Control(Page):
    form_model = 'player'
    form_fields = ['q_self_control_1', 'q_self_control_2', 'q_self_control_3', 'q_self_control_4',
                   'q_self_control_5', 'q_self_control_6', 'q_self_control_7', 'q_self_control_8',
                   'q_self_control_9', 'q_self_control_10', 'q_self_control_11', 'q_self_control_12',
                   'q_self_control_13']

class Game(Page):
    form_model = 'player'
    form_fields = ['q_gambling_1', 'q_gambling_2', 'q_gambling_3', 'q_gambling_4',
                   'q_gambling_5', 'q_gambling_6', 'q_gambling_7', 'q_gambling_8',
                   'q_gambling_9']


page_sequence = [General, Video_1, Video_2, Control, Game]
