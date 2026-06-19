from __future__ import annotations

from typing import Dict, Any, Optional

from models import UserProfile, EconomyState, RoundSession


class StateService:
    """
    Responsible for applying gameplay effects to:
    - UserProfile
    - EconomyState

    GameEngine should only calculate outcomes.
    StateService mutates persistent game state.
    """

    PROFILE_100_FIELDS = {
        "public_standing",
        "investor_standing",
        "institution_standing",
        "peer_standing",
        "leverage",
    }

    PROFILE_1_FIELDS = {
        "risk_appetite",
        "cooperation_bias",
        "clarity",
    }

    ECONOMY_100_FIELDS = {
        "trust",
        "resource_health",
        "market_heat",
        "regulatory_heat",
        "resilience",
        "volatility",
    }

    @staticmethod
    def clamp(value: float, min_value: float, max_value: float) -> float:
        return max(min_value, min(value, max_value))

    @classmethod
    def clamp_profile_field(cls, field_name: str, value: float) -> float:
        if field_name in cls.PROFILE_100_FIELDS:
            return cls.clamp(value, 0, 100)
        if field_name in cls.PROFILE_1_FIELDS:
            return cls.clamp(value, 0.0, 1.0)
        return value

    @classmethod
    def clamp_economy_field(cls, field_name: str, value: float) -> float:
        if field_name in cls.ECONOMY_100_FIELDS:
            return cls.clamp(value, 0, 100)
        return value

    @staticmethod
    async def get_or_create_economy_state(session: RoundSession) -> EconomyState:
        """
        Finds the EconomyState for the given round session.
        If none exists, creates one with safe defaults.
        """
        state = await EconomyState.find_one(EconomyState.session.id == session.id)

        if state:
            return state

        state = EconomyState(
            session=session,
            market_id=session.market_id,
            round_number=session.round_number if hasattr(session, "round_number") else 0,
            trust=50,
            resource_health=50,
            market_heat=50,
            regulatory_heat=50,
            resilience=50,
            volatility=50,
        )
        await state.insert()
        return state

    @staticmethod
    async def get_profile_by_user_id(user_id: int) -> Optional[UserProfile]:
        return await UserProfile.find_one(UserProfile.user.id == user_id)

    @classmethod
    def apply_effects_to_profile(
        cls,
        profile: UserProfile,
        effects: Dict[str, Any]
    ) -> UserProfile:
        """
        Applies effect deltas to a user profile in memory.
        Does not save automatically.
        """
        for field_name, delta in effects.items():
            if not hasattr(profile, field_name):
                continue

            current_value = getattr(profile, field_name, 0)
            if current_value is None:
                current_value = 0

            new_value = current_value + delta
            new_value = cls.clamp_profile_field(field_name, new_value)

            setattr(profile, field_name, new_value)

        return profile

    @classmethod
    def apply_effects_to_economy(
        cls,
        economy: EconomyState,
        effects: Dict[str, Any]
    ) -> EconomyState:
        """
        Applies economy deltas in memory.
        Does not save automatically.
        """
        for field_name, delta in effects.items():
            if not hasattr(economy, field_name):
                continue

            current_value = getattr(economy, field_name, 0)
            if current_value is None:
                current_value = 0

            new_value = current_value + delta
            new_value = cls.clamp_economy_field(field_name, new_value)

            setattr(economy, field_name, new_value)

        return economy

    @classmethod
    async def apply_pvp_outcome(
        cls,
        session: RoundSession,
        players: list,
        outcome: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Applies a PvP game outcome to:
        - each player's UserProfile
        - the shared EconomyState for this session

        Expected outcome shape:
        {
            "scores": {123: 2, 456: -1},
            "effects": {
                123: {"public_standing": 2},
                456: {"peer_standing": -3},
                "economy": {"trust": -4}
            },
            "mode": "NEGOTIATION"
        }
        """
        effects = outcome.get("effects", {})
        scores = outcome.get("scores", {})

        economy = await cls.get_or_create_economy_state(session)
        economy_effects = effects.get("economy", {})
        cls.apply_effects_to_economy(economy, economy_effects)

        updated_profiles = []

        for player in players:
            user_id = player["id"]

            profile = await cls.get_profile_by_user_id(user_id)
            if not profile:
                continue

            player_effects = effects.get(user_id, {})

            cls.apply_effects_to_profile(profile, player_effects)

            # اگر بعداً خواستی score cumulative نگه داری،
            # اینجا فیلدی مثل total_score را هم آپدیت کن
            if hasattr(profile, "total_score"):
                current_score = getattr(profile, "total_score", 0) or 0
                setattr(profile, "total_score", current_score + scores.get(user_id, 0))

            if hasattr(profile, "total_decisions"):
                profile.total_decisions = (profile.total_decisions or 0) + 1

            # counters اختیاری رفتاری
            # این‌ها را بر اساس outcome/mode بعداً می‌توان دقیق‌تر کرد
            updated_profiles.append(profile)

        # save all profiles
        for profile in updated_profiles:
            await profile.save()

        await economy.save()

        return {
            "applied": True,
            "mode": outcome.get("mode"),
            "economy_effects": economy_effects,
            "scores": scores,
        }

    @classmethod
    async def apply_solo_effects(
        cls,
        session: RoundSession,
        user_id: int,
        profile_effects: Dict[str, Any],
        economy_effects: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        For scenario/decision based solo gameplay.
        Applies profile effects to one user and optional economy effects.
        """
        economy_effects = economy_effects or {}

        profile = await cls.get_profile_by_user_id(user_id)
        if not profile:
            return {
                "applied": False,
                "reason": "profile_not_found",
                "user_id": user_id,
            }

        economy = await cls.get_or_create_economy_state(session)

        cls.apply_effects_to_profile(profile, profile_effects)
        cls.apply_effects_to_economy(economy, economy_effects)

        if hasattr(profile, "total_decisions"):
            profile.total_decisions = (profile.total_decisions or 0) + 1

        await profile.save()
        await economy.save()

        return {
            "applied": True,
            "user_id": user_id,
            "profile_effects": profile_effects,
            "economy_effects": economy_effects,
        }
