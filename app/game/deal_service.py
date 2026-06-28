import uuid
from datetime import datetime
from app.data.models import Deal, DealStatusEnum


class DealService:

    async def create_deal(
        self,
        proposer,
        receiver,
        market_id,
        scenario=None,
        session=None,
        deal_type="investment",
        required_capital=0,
        expected_return=0,
        risk_level=0.3,
        trust_requirement=50,
    ):

        deal = Deal(
            deal_key=str(uuid.uuid4()),
            proposer=proposer,
            receiver=receiver,
            scenario=scenario,
            session=session,
            market_id=market_id,
            deal_type=deal_type,
            required_capital=required_capital,
            expected_return=expected_return,
            risk_level=risk_level,
            trust_requirement=trust_requirement,
            status=DealStatusEnum.pending,
        )

        await deal.insert()
        return deal

    async def accept_deal(self, deal_id, user_id=None):

        deal = await Deal.get(deal_id)

        if not deal or deal.status != DealStatusEnum.pending:
            return {"ok": False, "reason": "deal_not_found_or_not_pending"}

        deal.status = DealStatusEnum.accepted
        await deal.save()

        return {"ok": True, "deal": deal}

    async def reject_deal(self, deal_id, user_id=None):

        deal = await Deal.get(deal_id)

        if not deal:
            return {"ok": False, "reason": "deal_not_found"}

        deal.status = DealStatusEnum.rejected
        await deal.save()

        return {"ok": True, "deal": deal}

    async def accept_and_resolve_deal(self, deal_id, user_id=None):
        deal = await Deal.get(deal_id)

        if not deal or deal.status != DealStatusEnum.pending:
            return {"ok": False, "reason": "deal_not_found_or_not_pending"}

        deal.status = DealStatusEnum.accepted
        await deal.save()

        outcome = {
            "success": True,
            "message": "Deal accepted and resolved.",
            "profile_effects": {"balance": deal.expected_return - deal.required_capital},
        }

        return {"ok": True, "deal": deal, "outcome": outcome}
