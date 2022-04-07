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
from .exception import PaymentKeyNotFound
from .payout_url_generator import PayoutURLGenerator

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'payment'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    def creating_session(self):
        payment_keys = ['expId', 'expShortName']
        for k in payment_keys:
            if k not in self.session.config.keys():
                raise PaymentKeyNotFound(k)


    def vars_for_admin_report(self):
        participants = self.session.get_participants()
        total_payoff_all = sum([p.payoff.to_real_world_currency(self.session) for p in participants])
        mean_payoff_all = total_payoff_all/self.session.num_participants

        # base url added directly in template
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
    orsee_id = models.StringField(label="Please enter your participant ID:")

    def create_paymentURL(self):
        """
        
        Small helper function to create a payment URL.
        """
        expShortName = self.session.config['expShortName']
        expId = self.session.config['expId']
        pid = self.participant.label
        final_payoff = float(self.participant.payoff_plus_participation_fee())
        paymentURL = PayoutURLGenerator(expShortName,
                                        expId,
                                        pid,
                                        final_payoff).getPayoutURL()
        return paymentURL