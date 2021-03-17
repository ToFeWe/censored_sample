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
    q_semester = models.StringField(label='Falls Sie noch studieren: Im wievielten Semester studieren Sie?', blank=True)
    q_n_experiment = models.IntegerField(label='An wie vielen Experimenten haben Sie (ungefähr) bereits teilgenommen?', max=500, min=0)
    q_similar_experiment = models.StringField(label='Haben Sie schon einmal an einem ähnlichen Experiment teilgenommen?',
                                         choices=['Ja.', 'Nein.', 'Ich weiß es nicht.'])


    q_abitur = models.FloatField(label="Was war die Abschlussnote Ihres letzten Schulabschlusses (1,0 - 4,0)?", min=1.0, max=6.0)
    q_math = models.FloatField(label="Was war Ihre letze Mathenote (1,0 - 6,0)?", min=1.0, max=6.0)
    q_budget = models.IntegerField(label="Wie viel Geld haben Sie monatlich (nach Abzug von Fixkosten wie Miete, Versicherungen etc.) zur Verfügung?",
                                   min=0, max=1000000)
    q_spending = models.IntegerField(label="Wie viel Geld geben Sie monatlich aus (nach Abzug von Fixkosten wie Miete, Versicherungen etc.)?",
                                   min=0, max=1000000)
    
    # Falk Questions
    # Risk
    q_falk1 = models.IntegerField(
        initial=None,
        choices=list(range(11)), # gar nicht risikobereit - sehr risikobereit
        label='Sind Sie im Allgemeinen ein risikobereiter Mensch oder versuchen Sie, Risiken zu vermeiden?',
        widget=widgets.RadioSelectHorizontal())

    # Time
    q_falk2 = models.CharField(
        initial=None,
        choices=[('0', 'gar nicht bereit zu verzichten'),
                 ('1', ''),
                 ('2', ''),
                 ('3', ''),
                 ('4', ''),
                 ('5', ''),
                 ('6', ''),
                 ('7', ''),
                 ('8', ''),
                 ('9', ''),
                 ('10', 'sehr bereit zu verzichten')],
        verbose_name='Sind Sie im Vergleich zu anderen im Allgemeinen bereit heute auf etwas zu verzichten, um in der Zukunft davon zu profitieren oder sind Sie im Vergleich zu anderen dazu nicht bereit?',
        doc="""Sind Sie im Vergleich zu anderen im Allgemeinen bereit heute auf etwas zu verzichten, um in der Zukunft davon zu profitieren oder sind Sie im Vergleich zu anderen dazu nicht bereit?""",
        widget=widgets.RadioSelectHorizontal())

    # Trust
    q_falk3 = models.CharField(
        initial=None,
        choices=[('0', 'trifft gar nicht zu'),
                 ('1', ''),
                 ('2', ''),
                 ('3', ''),
                 ('4', ''),
                 ('5', ''),
                 ('6', ''),
                 ('7', ''),
                 ('8', ''),
                 ('9', ''),
                 ('10', 'trifft voll zu')],
        verbose_name='Solange man mich nicht vom Gegenteil überzeugt, gehe ich stets davon aus, dass andere Menschen nur das Beste im Sinn haben.',
        doc="""Solange man mich nicht vom Gegenteil überzeugt, gehe ich stets davon aus, dass andere Menschen nur das Beste im Sinn haben.""",
        widget=widgets.RadioSelectHorizontal())

    # Neg. Rec.
    q_falk4 = models.CharField(
        initial=None,
        choices=[('0', 'gar nicht bereit zu bestrafen'),
                 ('1', ''),
                 ('2', ''),
                 ('3', ''),
                 ('4', ''),
                 ('5', ''),
                 ('6', ''),
                 ('7', ''),
                 ('8', ''),
                 ('9', ''),
                 ('10', 'sehr bereit zu bestrafen')],
        verbose_name='Sind Sie jemand, der im Allgemeinen bereit ist, unfaires Verhalten zu bestrafen, auch wenn das für Sie mit Kosten verbunden ist, oder sind Sie dazu nicht bereit?',
        doc="""Sind Sie jemand, der im Allgemeinen bereit ist, unfaires Verhalten zu bestrafen, auch wenn das für Sie mit Kosten verbunden ist, oder sind Sie dazu nicht bereit?""",
        widget=widgets.RadioSelectHorizontal())

    # Pos. Rec.
    q_falk5 = models.CharField(
        initial=None,
        choices=[('0', 'trifft gar nicht zu'),
                 ('1', ''),
                 ('2', ''),
                 ('3', ''),
                 ('4', ''),
                 ('5', ''),
                 ('6', ''),
                 ('7', ''),
                 ('8', ''),
                 ('9', ''),
                 ('10', 'trifft voll zu')],
        verbose_name='Wenn mir jemand einen Gefallen tut, bin ich bereit, diesen zu erwidern.',
        doc="""Wenn mir jemand einen Gefallen tut, bin ich bereit, diesen zu erwidern.""",
        widget=widgets.RadioSelectHorizontal())

    # Alturism
    q_falk6 = models.IntegerField(
        initial=None, min=0, max=1000,
        verbose_name='Stellen Sie sich folgende Situation vor: Sie haben in einem Preisausschreiben 1.000 € gewonnen. Wie viel würden Sie in Ihrer momentanen Situation für einen gemeinnützigen Zweck spenden?',
        doc="""Stellen Sie sich folgende Situation vor: Sie haben in einem Preisausschreiben 1.000 € gewonnen. Wie viel würden Sie in Ihrer momentanen Situation für einen gemeinnützigen Zweck spenden?""")
