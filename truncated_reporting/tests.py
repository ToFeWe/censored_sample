from otree.api import Currency as c, currency_range, SubmissionMustFail, expect
from . import pages
from ._builtin import Bot
from .models import Constants
import random

class PlayerBot(Bot):
    def play_round(self):
        if self.round_number == 1:
            if self.player.treatment == 'BEST' or self.player.treatment == 'BEST_INFO' or self.player.treatment == 'BEST_NUDGE':
                expect('Sie erhalten nicht die volle Information', 'in', self.html)
                expect('fünf Züge aus der jeweiligen Lotterie', 'in', self.html)
            elif self.player.treatment == 'FULL':
                expect('Sie erhalten nicht die volle Information', 'not in', self.html)
                expect('fünf Züge aus der jeweiligen Lotterie', 'not in', self.html)
            else:
                raise Exception('what the fuck is this treatment?! ->', self.player.treatment)

            yield pages.Introduction
        
        current_lottery = self.player.lottery
        max_pay = max(Constants.all_lotteries[current_lottery]['dist'].keys())
        min_pay = min(Constants.all_lotteries[current_lottery]['dist'].keys())
        ev = int(sum(k*v for k,v in Constants.all_lotteries[current_lottery]['dist'].items()))
        sum_probs = sum(v for v in Constants.all_lotteries[current_lottery]['dist'].values())
        assert sum_probs == 1, "probabilities don't sum up"

        rand_error = random.randint(-10,10)
        wtp_submission = ev + rand_error
        if wtp_submission < 0:
            wtp_submission = 0
        if self.player.treatment == 'TRUNCATED':
            expect('nicht die volle Information', 'in', self.html)
            wtp_submission += 5
        elif self.player.treatment == 'BEST':
            expect('fünf Züge mit der höchsten', 'in', self.html)
            wtp_submission += 15
        elif self.player.treatment == 'BEST_INFO' or self.player.treatment == 'BEST_NUDGE':
            expect('fünf Züge mit der höchsten', 'in', self.html)
            wtp_submission += 8

        expect(str(max_pay), 'in', self.html)
        expect(str(min_pay), 'in', self.html)
        middle_prob = Constants.all_lotteries[current_lottery]['dist'][
                        list(Constants.all_lotteries[current_lottery]['dist'].keys())[1]
                      ]
        if self.player.treatment in ['FULL', 'FULL_BEST']:
            expect(str(int(round(middle_prob*100)))+ '% genau', 'in', self.html)
        else:
            expect(str(int(round(middle_prob*100))) + '% genau', 'not in', self.html)
            expect('Wahrscheinlichkeit mindestens', 'in', self.html)
        yield SubmissionMustFail(pages.Decision, dict(wtp_lottery=max_pay+1))
        yield SubmissionMustFail(pages.Decision, dict(wtp_lottery=min_pay-1))
        yield pages.Decision, dict(wtp_lottery=wtp_submission)

        if self.round_number == Constants.num_rounds:
            if self.player.treatment in ['BEST', 'BEST_NUDGE', 'BEST_INFO']:
                # First lottery should be the same as the belief lottery
                assert self.player.in_round(1).lottery == self.player.lottery_for_belief

                max_lottery_value = max(list(Constants.all_lotteries[self.player.lottery_for_belief]['dist'].keys()))
                expect(str(max_lottery_value), 'in', self.html)

                max_prob_to_allocate = 1 - max(list(Constants.all_lotteries[self.player.lottery_for_belief]['dist'].values()))
                max_prob_scaled = int(round(max_prob_to_allocate * 100))

                yield SubmissionMustFail(pages.Belief, dict(belief=max_prob_scaled+1))

                # Equal participant id answer correctly and the others not
                if self.participant.id_in_session % 2:
                    yield pages.Belief, dict(belief=1)
                    expect(self.player.belief_bonus_won, True)
                    expect(self.player.win_probability, 1)
                else:
                    if self.participant.id_in_session % 3:
                        yield pages.Belief, dict(belief=7)
                        expected_win_prob = 1 - abs(7 - 1) / max_prob_scaled
                        expect(self.player.win_probability, expected_win_prob)
                        print(expected_win_prob)
                    else:
                        yield pages.Belief, dict(belief=2)
                        expected_win_prob = 1 - abs(2 - 1) / max_prob_scaled
                        expect(self.player.win_probability, expected_win_prob)
                        print(expected_win_prob)
