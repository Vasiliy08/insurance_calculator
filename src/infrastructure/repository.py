import copy
from datetime import datetime

from sqlalchemy import desc, func, select

from src.exceptions.rate import InvalidDateException, RateNotFoundException
from src.infrastructure.db_helper import DatabaseHelper
from src.infrastructure.models.rate import Rate


class RateRepository(DatabaseHelper):
    async def update_rates_in_db(self, rates_data: dict):
        async with self.session_factory() as session:
            old_rate = {}
            for date_str, rates in rates_data.items():
                try:
                    effective_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                except ValueError:
                    raise InvalidDateException(date=date_str)
                for rate in rates:
                    cargo_type = rate["cargo_type"]
                    rate_value = float(rate["rate"])

                    result = await session.execute(
                        select(Rate).where(Rate.cargo_type == cargo_type, Rate.effective_date == effective_date)
                    )
                    existing_rate = result.scalars().first()
                    if existing_rate and existing_rate.rate != rate_value:
                        old_rate.setdefault(copy.deepcopy(existing_rate), rate_value)
                        existing_rate.rate = rate_value
                    else:
                        new_rate = Rate(cargo_type=cargo_type, rate=rate_value, effective_date=effective_date)
                        session.add(new_rate)

            await session.commit()
            return old_rate

    async def calculate_insurance(self, cargo_type: str, declared_value: float, date: str):
        async with self.session_factory() as session:
            rate = await session.execute(
                select(Rate)
                .where(Rate.cargo_type == cargo_type, Rate.effective_date <= date)
                .order_by(Rate.effective_date.desc())
            )
            rate = rate.scalars().first()

            if rate is None:
                raise RateNotFoundException(cargo_type=cargo_type, date=date)

            insurance_cost = declared_value * rate.rate
            return insurance_cost

    async def get_all_rates(self, pagination):
        async with self.session_factory() as session:
            query = select(Rate).limit(pagination.limit).offset(pagination.offset)
            if pagination.order_by == "asc":
                rates = await session.execute(query)
                return rates.scalars().all()
            rates = await session.execute(query.order_by(desc(Rate.oid)))
            return rates.scalars().all()

    async def get_count_rate(self):
        async with self.session_factory() as session:
            count = await session.scalar(select(func.count()).select_from(Rate))
            return count

    async def delete_rate(self, cargo_type: str, effective_date: str):
        async with self.session_factory() as session:
            rate = await session.execute(
                select(Rate).where(Rate.cargo_type == cargo_type, Rate.effective_date == effective_date)
            )
            existing_rate = rate.scalars().first()
            if existing_rate:
                await session.delete(existing_rate)
                await session.commit()
            else:
                raise RateNotFoundException(cargo_type=cargo_type, date=effective_date)

    async def edit_rate(
        self,
        cargo_type: str,
        effective_date: str,
        new_rate_value: float,
    ):
        async with self.session_factory() as session:
            rate = await session.execute(
                select(Rate).where(Rate.cargo_type == cargo_type, Rate.effective_date == effective_date)
            )
            existing_rate = rate.scalars().first()
            if existing_rate:
                old_rate = existing_rate.rate
                existing_rate.rate = new_rate_value
                await session.commit()
            else:
                raise RateNotFoundException(cargo_type=cargo_type, date=effective_date)

            return old_rate
