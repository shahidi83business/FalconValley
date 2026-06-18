import uuid
from datetime import datetime
from models import Deal, DealStatus


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
            status=DealStatus.pending,
        )

        await deal.insert()
        return deal

    async def accept_deal(self, deal_id):

        deal = await Deal.get(deal_id)

        if not deal or deal.status != DealStatus.pending:
            return None

        deal.status = DealStatus.accepted
        await deal.save()

        return deal

    async def reject_deal(self, deal_id):

        deal = await Deal.get(deal_id)

        if not deal:
            return None

        deal.status = DealStatus.rejected
        await deal.save()

        return deal
