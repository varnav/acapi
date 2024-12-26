from typing import Optional
from litestar import Litestar, get
from litestar.response import Response
from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column


# Database Model
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


# Database connection
DATABASE_URL = "sqlite:///./BaseStation.sqb"
engine = create_engine(DATABASE_URL)

@get("/api/v1/ac/dbinfo")
async def get_db_info() -> dict:
    with Session(engine) as session:
        row_count = session.execute(select(func.count()).select_from(Aircraft)).scalar()
        return {
            "rowcount": row_count
        }


@get("/api/v1/ac/reg/{registration:str}")
async def get_aircraft(registration: str) -> dict:
    """Look up aircraft by registration number."""
    with Session(engine) as session:
        stmt = select(Aircraft).where(Aircraft.Registration == registration.upper())
        result = session.execute(stmt).scalar_one_or_none()

        if not result:
            return Response(
                status_code=404,
                content={"error": f"No aircraft found with registration {registration}"}
            )

        return Response(
            content={
                "ModeS": result.ModeS,
                "Registration": result.Registration,
                "ICAOTypeCode": result.ICAOTypeCode,
                "OperatorFlagCode": result.OperatorFlagCode,
                "Manufacturer": result.Manufacturer,
                "Type": result.Type,
                "RegisteredOwners": result.RegisteredOwners
            },
            headers={"Cache-Control" : "public, max-age=300, immutable, stale-if-error=1800"}
        )


# Create the Litestar application
app = Litestar([get_aircraft, get_db_info])
