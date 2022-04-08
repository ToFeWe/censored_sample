from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)


doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'introduction'
    players_per_group = None
    num_rounds = 1
    time_to_finish = 8 # Minutes
    base_pay =  c(1.50)
    n_lotteries = 5

    # Some example lotteries
    auto_click_lottery = [(100,5), (50,60), (0,35)]
    auto_click_rhs = list(range(0,105,5))

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    attention_check = models.StringField(label="")
    attention_check_num = models.IntegerField()
    failed_attention = models.BooleanField()

    prolific_id = models.StringField(label="Your Prolific-ID:")


    # Comprehension questions

    comprehension_question_1 = models.IntegerField(label="", #1. Which one of the following statements is correct if the following lottery is played for you?
                                                  choices=[[1, "It is possible that I get paid both $100 and $50, i.e., I may receive a total amount of $150 from this lottery."],
                                                           [2, "I receive EITHER $100 OR $50 OR $0 from this lottery."],
                                                           [3, "I will receive at least some money with certainty."]], 
                                                  widget=widgets.RadioSelect)

    comprehension_question_2 = models.IntegerField(label="", #2. Suppose a person made the decisions shown in the choice list below. Which of the following statements is correct regarding these decisions?
                                                  choices=[[1, "This person indicated that the lottery is worth more to them than $65."],
                                                           [2, "This person indicated that the lottery is worth between $50 and $55 to them."],
                                                           [3, "This person indicated that the lottery is worth between $15 and $30 to them."]], 
                                                  widget=widgets.RadioSelect)
    comprehension_passed = models.BooleanField() 

    def validate_comprehension_questions(self):
        """ Validate if both comprehension questions have been answered correct. """
        both_correct =  (self.comprehension_question_1 == 2) & (self.comprehension_question_2 == 2)
        self.comprehension_passed = both_correct

        # Also write to participant variables as we have to access it in the next app
        # Note we only need to check the comprehension check in the next app and not
        # the attention check as the player would not arrive to the next app if he failed

        self.participant.vars['comprehension_passed'] = both_correct
        