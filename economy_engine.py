import random

from app.models.economy_state import EconomyState
from app.utils.economy import (
    calculate_prisoner_payoff,
    update_trust,
    calculate_reputation,
    predict_player_behavior,
    risk_utility,
    apply_uncertainty,
    risk_adjusted_payoff,
    perceived_risk,
    prospect_theory
)


class EconomyEngine:

    @classmethod
    def apply_decision(cls, session, decision, scenario):

        previous_state = cls._get_last_state(session)

        player_move = decision.selected_option
        opponent_move = cls._simulate_opponent(session)

        payoff_player, payoff_opponent = calculate_prisoner_payoff(
            player_move,
            opponent_move,
            scenario.payoff_params
        )

        payoff_player = apply_uncertainty(
            payoff_player,
            scenario.noise_params
        )

        risk_score = perceived_risk(
            previous_state.risk_level,
            scenario.risk_perception_params
        )

        payoff_player = risk_adjusted_payoff(
            payoff_player,
            risk_score,
            scenario.risk_adjustment_params
        )

        trust = update_trust(
            previous_state.trust,
            player_move,
            opponent_move,
            scenario.trust_params
        )

        history = cls._get_move_history(session)

        reputation = calculate_reputation(
            history + [player_move],
            scenario.reputation_params
        )

        predicted_coop = predict_player_behavior(
            history,
            scenario.prediction_params
        )

        utility = risk_utility(
            [payoff_player],
            [1.0],
            scenario.utility_params
        )

        prospect_value = prospect_theory(
            [payoff_player],
            [1.0],
            scenario.prospect_params
        )

        new_wealth = previous_state.wealth + payoff_player

        cooperation_rate = cls._calculate_cooperation_rate(history + [player_move])

        inequality = cls._calculate_inequality(session, new_wealth)

        new_state = EconomyState(
            session=session,
            round_number=previous_state.round_number + 1,
            wealth=new_wealth,
            trust=trust,
            reputation=reputation,
            cooperation=cooperation_rate,
            risk_level=risk_score,
            inequality=inequality,
            predicted_cooperation=predicted_coop,
            utility=utility,
            prospect_value=prospect_value
        )

        new_state.save()

        impact = {
            "wealth_change": new_wealth - previous_state.wealth,
            "trust_change": trust - previous_state.trust,
            "reputation_change": reputation - previous_state.reputation
        }

        return {
            "previous_state": previous_state,
            "new_state": new_state,
            "impact": impact
        }

    # -----------------------------

    @staticmethod
    def _get_last_state(session):

        state = EconomyState.objects(
            session=session
        ).order_by("-round_number").first()

        if state:
            return state

        return EconomyState(
            session=session,
            round_number=0,
            wealth=100,
            trust=0.5,
            reputation=50,
            cooperation=0.5,
            risk_level=0.5,
            inequality=0
        )

    # -----------------------------

    @staticmethod
    def _simulate_opponent(session):

        history = [
            d.selected_option
            for d in session.decisions.order_by("created_at")
        ]

        prediction = predict_player_behavior(
            history,
            {"depth": 3}
        )

        return 0 if random.random() < prediction else 1

    # -----------------------------

    @staticmethod
    def _get_move_history(session):

        return [
            d.selected_option
            for d in session.decisions.order_by("created_at")
        ]

    # -----------------------------

    @staticmethod
    def _calculate_cooperation_rate(history):

        if not history:
            return 0.5

        coop = history.count(0)

        return coop / len(history)

    # -----------------------------

    @staticmethod
    def _calculate_inequality(session, new_wealth):

        players = session.players

        wealth_values = [p.wealth for p in players]

        wealth_values.append(new_wealth)

        if not wealth_values:
            return 0

        avg = sum(wealth_values) / len(wealth_values)

        variance = sum((x - avg) ** 2 for x in wealth_values) / len(wealth_values)

        return variance
