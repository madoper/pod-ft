#!/usr/bin/env python3
__anchor__ = "source-registry"
# schema-ref: project-schema.yaml#/services/2
# Seed Tier-1 source domains into the database

import asyncio

from backend.shared.db.postgres import async_session_factory

TIER1_SOURCES = [
    {"domain": "fedsfm.ru", "source_type": "government",
     "regulator_name": "Росфинмониторинг", "tier": 1},
    {"domain": "cbr.ru", "source_type": "government",
     "regulator_name": "Банк России", "tier": 1},
    {"domain": "publication.pravo.gov.ru", "source_type": "government",
     "regulator_name": "Официальное опубликование", "tier": 1},
    {"domain": "minfin.ru", "source_type": "government",
     "regulator_name": "Минфин России", "tier": 1},
]


async def seed() -> None:
    async with async_session_factory() as session:
        for src in TIER1_SOURCES:
            await session.execute(
                __import__("sqlalchemy").text(
                    "INSERT INTO source_domains (domain, source_type, regulator_name, tier) "
                    "VALUES (:domain, :source_type, :regulator_name, :tier) "
                    "ON CONFLICT (domain) DO NOTHING"
                ),
                src,
            )
        await session.commit()
    print(f"Seeded {len(TIER1_SOURCES)} Tier-1 sources")


if __name__ == "__main__":
    asyncio.run(seed())
