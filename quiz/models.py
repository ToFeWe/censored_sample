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
    q_age = models.IntegerField(label='Wie alt sind Sie?', min=16, max=99)
    q_gender = models.StringField(
        label = 'Was ist Ihr Geschlecht?',
        choices = ['Männlich', 'Weiblich', 'Divers', 'keine Angabe']
    )

    q_study_level = models.StringField(
        choices=[
            "Weiterführende Schule nicht beendet",
            "Abitur",
            "Berufliche Qualifikation",
            "Bachelorabschluss",
            "Masterabschluss",
            "Promotion",
            'keine Angabe'],
        label='Was ist Ihr höchster Bildungsabschluss?')

    q_study_field = models.StringField(label='Was studieren Sie? / Was ist Ihre Tätigkeit?')
    q_semester = models.IntegerField(label='Falls Sie noch studieren: Im wievielten Semester studieren Sie?', blank=True, min=0)
    q_n_experiment = models.IntegerField(label='An wie vielen Experimenten haben Sie (ungefähr) bereits teilgenommen?', max=500, min=0)

    q_abitur = models.FloatField(label="Was war die Abschlussnote Ihres letzten Schulabschlusses (1,0 - 4,0)?", min=1.0, max=6.0)
    q_math = models.FloatField(label="Was war Ihre letzte Mathenote (1,0 - 6,0)?", min=1.0, max=6.0)
    q_budget = models.IntegerField(label="Wie viel Geld haben Sie monatlich (nach Abzug von Fixkosten wie Miete, Versicherungen etc.) zur Verfügung?",
                                   min=0, max=1000000)
    q_spending = models.IntegerField(label="Wie viel Geld geben Sie monatlich aus (nach Abzug von Fixkosten wie Miete, Versicherungen etc.)?",
                                   min=0, max=1000000)
    
    # Falk Questions
    # Risk
    q_falk_risk = models.IntegerField(
        initial=None,
        choices=list(range(11)), # gar nicht risikobereit - sehr risikobereit
        label='Sind Sie im Allgemeinen ein risikobereiter Mensch oder versuchen Sie, Risiken zu vermeiden?',
        widget=widgets.RadioSelectHorizontal())

    # Time
    q_falk_time = models.IntegerField(
        initial=None,
        choices=list(range(11)), # gar nicht bereit zu verzichten - sehr bereit zu verzichten
        label='Sind Sie im Vergleich zu anderen im Allgemeinen bereit heute auf etwas zu verzichten, um in der Zukunft davon zu profitieren oder sind Sie im Vergleich zu anderen dazu nicht bereit?',
        widget=widgets.RadioSelectHorizontal())

    # Trust
    q_falk_trust = models.IntegerField(
        initial=None,
        choices=list(range(11)), # trifft gar nicht zu - trifft voll zu
        label='Solange man mich nicht vom Gegenteil überzeugt, gehe ich stets davon aus, dass andere Menschen nur das Beste im Sinn haben.',
        widget=widgets.RadioSelectHorizontal())

    # Neg. Rec.
    q_falk_neg_rec = models.IntegerField(
        initial=None,
        choices=list(range(11)), # gar nicht bereit zu bestrafen - sehr bereit zu bestrafen
        label='Sind Sie jemand, der im Allgemeinen bereit ist, unfaires Verhalten zu bestrafen, auch wenn das für Sie mit Kosten verbunden ist, oder sind Sie dazu nicht bereit?',
        widget=widgets.RadioSelectHorizontal())

    # Pos. Rec.
    q_falk_pos_rec = models.IntegerField(
        initial=None,
        choices=list(range(11)), # trifft gar nicht zu - trifft voll zu
        label='Wenn mir jemand einen Gefallen tut, bin ich bereit, diesen zu erwidern.',
        widget=widgets.RadioSelectHorizontal())

    # Altruism
    q_falk_altruism = models.IntegerField(
        initial=None,
        min=0,
        max=1000,
        label='Stellen Sie sich folgende Situation vor: Sie haben in einem Preisausschreiben 1.000 € gewonnen. Wie viel würden Sie in Ihrer momentanen Situation für einen gemeinnützigen Zweck spenden?',
        )
