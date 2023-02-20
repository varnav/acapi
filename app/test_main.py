#!/usr/bin/env python3
import time
import os

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_version():
    response = client.get("/api/v1/version")
    assert response.status_code == 200


def test_aircraft():
    response = client.get("/api/v1/ac/getbyreg?reg=Z-WTV")
    assert response.status_code == 200
    assert response.json()[0] == {"ModeS": "004001",
                                  "Registration": "Z-WTV",
                                  "ICAOTypeCode": "IL76",
                                  "OperatorFlagCode": "SMJ",
                                  "Manufacturer": "ILYUSHIN",
                                  "Type": "Il-76T",
                                  "RegisteredOwners": "Avient"
                                  }
