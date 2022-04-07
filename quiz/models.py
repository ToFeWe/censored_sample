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


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'quiz'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # General Questions
    q_age = models.IntegerField(label='How old are you?', min=16, max=99)
    q_gender = models.StringField(
        label = 'What is your gender?',
        choices = ['Male', 'Female', 'Diverse', 'Prefer not to answer']
    )

    q_study_level = models.StringField(
        choices=[
            "Secondary school not completed",
            "High school graduation (Abitur)",
            "Professional qualification",
            "Bachelor's degree",
            "Master's degree",
            "PhD degree",
            'Prefer not to answer'],
        label='What is your highest level of education')

    q_study_field = models.StringField(label='What do you study? / What is your occupation?')
    q_semester = models.IntegerField(label='If you are studying: In which semester are you studying?', blank=True, min=0)
    q_n_experiment = models.IntegerField(label='How many experiments have you (roughly) already participated in?', max=500, min=0)

    q_abitur = models.FloatField(label="What was the final grade of your last graduation (1,0 - 4,0)?", min=1.0, max=6.0)
    q_math = models.FloatField(label="What was your last math grade (1,0 - 6,0)?", min=1.0, max=6.0)
    q_budget = models.IntegerField(label="How much money do you have available each month (after deducting fixed costs such as rent, insurance, etc.)?",
                                   min=0, max=1000000)
    q_spending = models.IntegerField(label="How much money do you spend each month (after deducting fixed costs such as rent, insurance, etc.)?",
                                   min=0, max=1000000)
    
    # Falk Questions
    # Risk
    q_falk_risk = models.IntegerField(
        initial=None,
        choices=list(range(11)), # gar nicht risikobereit - sehr risikobereit
        label='Are you in general a person who is willing to take risks or do you try to avoid them?',
        widget=widgets.RadioSelectHorizontal())

    # Time
    q_falk_time = models.IntegerField(
        initial=None,
        choices=list(range(11)), # gar nicht bereit zu verzichten - sehr bereit zu verzichten
        label='Compared to others, are you generally willing to give up something today in order to benefit in the future, or compared to others, are you unwilling to do so?',
        widget=widgets.RadioSelectHorizontal())

    # Trust
    q_falk_trust = models.IntegerField(
        initial=None,
        choices=list(range(11)), # trifft gar nicht zu - trifft voll zu
        label='Unless I am convinced otherwise, I always assume other people to have the best in mind.',
        widget=widgets.RadioSelectHorizontal())

    # Neg. Rec.
    q_falk_neg_rec = models.IntegerField(
        initial=None,
        choices=list(range(11)), # gar nicht bereit zu bestrafen - sehr bereit zu bestrafen
        label='Are you a person who is generally willing to punish someone for unfair behavior, even at cost for you, or are you not willing to do so?',
        widget=widgets.RadioSelectHorizontal())

    # Pos. Rec.
    q_falk_pos_rec = models.IntegerField(
        initial=None,
        choices=list(range(11)), # trifft gar nicht zu - trifft voll zu
        label='If someone does me a favor, I am willing to return it.',
        widget=widgets.RadioSelectHorizontal())

    # Altruism
    q_falk_altruism = models.IntegerField(
        initial=None,
        min=0,
        max=1000,
        label='Imagine the following situation: you won €1,000 in a competition. In your current situation, how much would you donate to charity?',
        )
