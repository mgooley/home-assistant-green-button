"""Tests for the ESPI Atom feed parser."""
from __future__ import annotations

import datetime

import pytest
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.const import UnitOfEnergy

from custom_components.green_button.parsers import espi

from .const import INVALID_XML
from .const import VALID_ESPI_XML
from .const import VALID_USAGE_POINT_ID


def test_parse_valid_feed() -> None:
    """A valid feed parses into a fully-populated UsagePoint."""
    usage_points = espi.parse_xml(VALID_ESPI_XML)

    assert len(usage_points) == 1
    usage_point = usage_points[0]
    assert usage_point.id == VALID_USAGE_POINT_ID
    assert usage_point.sensor_device_class is SensorDeviceClass.ENERGY

    meter_readings = list(usage_point.meter_readings)
    assert len(meter_readings) == 1
    meter_reading = meter_readings[0]
    assert meter_reading.reading_type.unit_of_measurement == UnitOfEnergy.WATT_HOUR
    assert meter_reading.reading_type.currency == "USD"
    assert meter_reading.reading_type.power_of_ten_multiplier == 0

    reading = meter_reading.get_newest_interval_reading()
    assert reading is not None
    assert reading.value == 100
    assert reading.cost == 1000
    assert reading.duration == datetime.timedelta(hours=1)
    assert reading.start == datetime.datetime(
        2021, 1, 1, tzinfo=datetime.timezone.utc
    )


def test_parse_invalid_xml_raises() -> None:
    """Malformed XML raises an EspiXmlParseError."""
    with pytest.raises(espi.EspiXmlParseError):
        espi.parse_xml(INVALID_XML)
