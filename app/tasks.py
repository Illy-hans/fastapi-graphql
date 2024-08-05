from celery_config import app
import asyncio
from app.db.session import get_session
from app.resolver.balance.balance_mutation_resolver import all_daily

@app.task()
def calculate_daily_balances():
    async def run_daily():
        async with get_session() as session:
            return await all_daily(session)
    
    return asyncio.get_event_loop().run_until_complete(run_daily())

