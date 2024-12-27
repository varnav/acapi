from typing import Optional, Any
from functools import lru_cache
from pydantic import BaseModel, constr
from litestar import Litestar, get, Response
from litestar.response import Response
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Aircraft(Base):
    __tablename__ = "Aircraft"

    ModeS: Mapped[str] = mapped_column(primary_key=True)
    Registration: Mapped[str] = mapped_column(index=True)
    ICAOTypeCode: Mapped[Optional[str]]
    OperatorFlagCode: Mapped[Optional[str]]
    Manufacturer: Mapped[Optional[str]]
    Type: Mapped[Optional[str]]
    RegisteredOwners: Mapped[Optional[str]]


class AircraftResponse(BaseModel):
    ModeS: str
    Registration: constr(pattern="^[A-Z0-9-]+$")
    ICAOTypeCode: Optional[str]
    OperatorFlagCode: Optional[str]
    Manufacturer: Optional[str]
    Type: Optional[str]
    RegisteredOwners: Optional[str]


DATABASE_URL = "sqlite+aiosqlite:///./BaseStation.sqb"
engine = create_async_engine(DATABASE_URL)
session = AsyncSession(engine)


@get("/api/v1/ac/dbinfo")
async def get_db_info() -> dict:
    result = await session.execute(select(func.count()).select_from(Aircraft))
    row_count = result.scalar()
    return {
        "rowcount": row_count
    }


@get("/api/v1/ac/reg/{registration:str}")
async def get_aircraft(registration: str) -> Response[dict[str, str]] | Response[dict[str, Any]]:
    """Look up aircraft by registration number."""
    stmt = select(Aircraft).where(Aircraft.Registration == registration.upper())
    result = await session.execute(stmt)
    aircraft = result.scalar_one_or_none()

    if not aircraft:
        return Response(
            status_code=404,
            content={"error": f"No aircraft found with registration {registration}"}
        )

    return Response(
        content=AircraftResponse(
            ModeS=aircraft.ModeS,
            Registration=aircraft.Registration,
            ICAOTypeCode=aircraft.ICAOTypeCode,
            OperatorFlagCode=aircraft.OperatorFlagCode,
            Manufacturer=aircraft.Manufacturer,
            Type=aircraft.Type,
            RegisteredOwners=aircraft.RegisteredOwners
        ).dict(),
        headers={"Cache-Control": "public, max-age=300, immutable, stale-if-error=1800"}
    )


app = Litestar([get_aircraft, get_db_info])