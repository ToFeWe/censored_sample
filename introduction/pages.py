from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class AttentionCheck(Page):
    form_model = 'player'
    form_fields = ['attention_check']

    def before_next_page(self):
        # count number of words for attention answer
        self.player.attention_check_num = len(self.player.attention_check.split())
        
        # check if participants failed attention check
        self.player.failed_attention =  self.player.attention_check_num < 15
        self.participant.vars['failed_attention'] = self.player.failed_attention

        # Assign participant label as orsee ID
        self.player.prolific_id = self.participant.label 


class AttentionCheckFail(Page):
    def is_displayed(self):
        return self.player.failed_attention

class Welcome(Page):
    form_model = 'player'
    form_fields = ['prolific_id']


class Instructions_1(Page):
    def vars_for_template(self):
        return self.player.get_general_instruction_vars()

class Comprehension(Page):
    form_model = 'player'
    form_fields = ['comprehension_question_1',
                   'comprehension_question_2']
    def before_next_page(self):
        self.player.validate_comprehension_questions()


class ComprehensionFail(Page):
    def is_displayed(self):
        return not self.player.comprehension_passed

    def app_after_this_page(self, upcoming_apps):
        # We skip the next app (price list)
        # if the participant failed to answer the 
        # comprehension questions.
        
        # If statement such that bots dont fail
        # If testes in isolation
        if len(upcoming_apps) >= 1:
            if not self.player.comprehension_passed:
                return upcoming_apps[-1]


class StartExperiment(Page):
    def is_displayed(self):
        return self.player.comprehension_passed

page_sequence = [AttentionCheck, AttentionCheckFail, 
                 Welcome, Instructions_1, 
                 Comprehension, ComprehensionFail,
                 StartExperiment]
