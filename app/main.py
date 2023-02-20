#!/usr/bin/env python3
import logging
from typing import List

from fastapi import FastAPI, Depends, Response, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, String, select
from sqlalchemy.orm import sessionmaker, Mapped, DeclarativeBase, mapped_column, Session

DATABASE_URL = "sqlite:///./BaseStation.sqb"

engine = create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


__version__ = '0.1.0'

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


# FastAPI declarations

class Version(BaseModel):
    ver: str = __version__


class Aircraft(BaseModel):
    ModeS: str
    Registration: str
    ICAOTypeCode: str
    OperatorFlagCode: str
    Manufacturer: str
    Type: str
    RegisteredOwners: str

    class Config:
        orm_mode = True


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
        raise HTTPException(status_code=500, detail="Not found")
