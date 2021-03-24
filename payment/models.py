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
    name_in_url = 'payment'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    def vars_for_admin_report(self):
        participants = self.session.get_participants()
        total_payoff_all = sum([p.payoff.to_real_world_currency(self.session) for p in participants])
        mean_payoff_all = total_payoff_all/self.session.num_participants

        
        urls_with_id = [
                p._start_url() + "/?participant_label=[TEILNEHMER-ID_EINFÜGEN]"
             for p in participants
        ]

        return {
            'urls_with_id': urls_with_id,
            'participants': participants,
            'total_payoff_all': total_payoff_all,
            'mean_payoff_all': mean_payoff_all
        }


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    orsee_id = models.StringField(label="Bitte geben Sie Ihre Teilnehmer-ID ein:")
