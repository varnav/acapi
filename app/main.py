#!/usr/bin/env python3
import logging
from typing import List

from fastapi import FastAPI, Depends, Response, HTTPException
from pydantic import ConfigDict, BaseModel
from sqlalchemy import create_engine, String, select, func, StaticPool
from sqlalchemy.orm import sessionmaker, Mapped, DeclarativeBase, mapped_column, Session

DATABASE_URL = "sqlite:///./BaseStation.sqb"

# Since DB is read-only, we can use StaticPool - single connection between all threads
engine = create_engine(DATABASE_URL, echo=True, pool_pre_ping=True,poolclass=StaticPool)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


__version__ = '0.3.0'

app = FastAPI(title="acapi", version=__version__, openapi_url="/api/v1/openapi.json")

print("Starting acapi", __version__)

log_formatter = logging.Formatter(
    '%(levelname)s %(asctime)-20s:\t %(message)s')
logger = logging.getLogger()
verbose = False
if verbose:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

# Setup the logger to write into file
file_handler = logging.FileHandler('web.log')
file_handler.setFormatter(log_formatter)
logger.addHandler(file_handler)

# Setup the logger to write into stdout
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)
logger.addHandler(console_handler)


# @app.middleware("http")
# def add_process_time_header(request: Request, call_next):
#     start_time = time.time()
#     response = await call_next(request)
#     process_time = time.time() - start_time
#     response.headers["Process-Time"] = str(process_time)
#     return response

# SQLAlchemy declarations

class Base(DeclarativeBase):
    pass


class AircraftDB(Base):
    __tablename__ = "Aircraft"

    ModeS: Mapped[str] = mapped_column(String, primary_key=True)
    Registration: Mapped[str] = mapped_column(String)
    ICAOTypeCode: Mapped[str] = mapped_column(String)
    OperatorFlagCode: Mapped[str] = mapped_column(String)
    Manufacturer: Mapped[str] = mapped_column(String)
    Type: Mapped[str] = mapped_column(String)
    RegisteredOwners: Mapped[str] = mapped_column(String)


# class FAADB(Base):
#     __tablename__ = "faadb"
#
#   NNumber: Mapped[str] = mapped_column(String, primary_key=True)
#   "SERIAL NUMBER: Mapped[str] = mapped_column(String)
#   "MFR MDL CODE: Mapped[str] = mapped_column(String)
#   "ENG MFR MDL: Mapped[str] = mapped_column(String)
#   "YEAR MFR: Mapped[str] = mapped_column(String)
#   "TYPE REGISTRANT: Mapped[str] = mapped_column(String)
#   "NAME: Mapped[str] = mapped_column(String)
#   "STREET: Mapped[str] = mapped_column(String)
#   "STREET2: Mapped[str] = mapped_column(String)
#   "CITY: Mapped[str] = mapped_column(String)
#   "STATE: Mapped[str] = mapped_column(String)
#   "ZIP CODE: Mapped[str] = mapped_column(String)
#   "REGION: Mapped[str] = mapped_column(String)
#   "COUNTY: Mapped[str] = mapped_column(String)
#   "COUNTRY: Mapped[str] = mapped_column(String)
#   "LAST ACTION DATE: Mapped[str] = mapped_column(String)
#   "CERT ISSUE DATE: Mapped[str] = mapped_column(String)
#   "CERTIFICATION: Mapped[str] = mapped_column(String)
#   "TYPE AIRCRAFT: Mapped[str] = mapped_column(String)
#   "TYPE ENGINE: Mapped[str] = mapped_column(String)
#   "STATUS CODE: Mapped[str] = mapped_column(String)
#   "MODE S CODE: Mapped[str] = mapped_column(String)
#   "FRACT OWNER: Mapped[str] = mapped_column(String)
#   "AIR WORTH DATE: Mapped[str] = mapped_column(String)
#   "OTHER NAMES(1): Mapped[str] = mapped_column(String)
#   "OTHER NAMES(2): Mapped[str] = mapped_column(String)
#   "OTHER NAMES(3): Mapped[str] = mapped_column(String)
#   "OTHER NAMES(4): Mapped[str] = mapped_column(String)
#   "OTHER NAMES(5): Mapped[str] = mapped_column(String)
#   "EXPIRATION DATE: Mapped[str] = mapped_column(String)
#   "UNIQUE ID: Mapped[str] = mapped_column(String)
#   "KIT MFR: Mapped[str] = mapped_column(String)
#   " KIT MODEL: Mapped[str] = mapped_column(String)
#   "MODE S CODE HEX: Mapped[str] = mapped_column(String)

# FastAPI declarations

class Version(BaseModel):
    ver: str = __version__


class DBInfo(BaseModel):
    # date: str
    rowcount: int


class Aircraft(BaseModel):
    ModeS: str
    Registration: str
    ICAOTypeCode: str
    OperatorFlagCode: str
    Manufacturer: str
    Type: str
    RegisteredOwners: str
    model_config = ConfigDict(from_attributes=True)


@app.get("/api/v1/version", response_model=Version, summary="Return version information")
def version():
    return {"ver": __version__}


@app.get("/api/v1/ac/getbyreg", response_model=List[Aircraft], summary="Return aircraft data")
def get_ac_by_reg(reg: str, response: Response, db: Session = Depends(get_db)):
    response.headers["Cache-Control"] = "public, max-age=300, immutable, stale-if-error=1800"
    qr = db.execute(select(AircraftDB).where(AircraftDB.Registration == reg.upper())).scalars().all()
    if len(qr) > 0:
        return qr
    else:
        raise HTTPException(status_code=404, detail="Not found")


@app.get("/api/v1/ac/dbinfo", response_model=DBInfo, summary="Return database information")
def get_ac_dbinfo(response: Response, db: Session = Depends(get_db)):
    response.headers["Cache-Control"] = "public, max-age=300, immutable, stale-if-error=1800"
    qr = db.execute(select(func.count(AircraftDB.ModeS))).scalar_one()
    if qr > 0:
        return {"rowcount": qr}
    else:
        raise HTTPException(status_code=500, detail="Not found")
