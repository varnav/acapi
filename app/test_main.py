#!/usr/bin/env python3
import time
import os

from litestar.status_codes import HTTP_200_OK
from litestar.testing import TestClient
from app import app

app.debug = True

client = TestClient(app)

# def test_version():
#     response = client.get("/api/v1/version")
#     assert response.status_code == 200

def test_dbinfo():
    response = client.get("/api/v1/ac/dbinfo")
    assert response.status_code == HTTP_200_OK


def test_aircraft():
    response = client.get("/api/v1/ac/reg/Z-WTV")
    assert response.status_code == HTTP_200_OK
    assert response.json() == {"ModeS": "004001",
                                  "Registration": "Z-WTV",
                                  "ICAOTypeCode": "IL76",
                                  "OperatorFlagCode": "SMJ",
                                  "Manufacturer": "ILYUSHIN",
                                  "Type": "Il-76T",
                                  "RegisteredOwners": "Avient"
                                  }
    
# def test_aircraft():
#     response = client.get("/api/v1/acn/getbyreg?reg=Z-WTV")
#     assert response.status_code == 200
#     assert response.json()[0] == {"ModeS": "004001",
#                                   "Registration": "Z-WTV",
#                                   "ICAOTypeCode": "IL76",
#                                   "OperatorFlagCode": "SMJ",
#                                   "Manufacturer": "ILYUSHIN",
#                                   "Type": "Il-76T",
#                                   "RegisteredOwners": "Avient"
#                                   }
