"""Test the Green Button config flow."""

from __future__ import annotations

from unittest.mock import patch

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType
import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.green_button.const import DOMAIN

from .const import EMPTY_FEED_XML, INVALID_XML, VALID_ESPI_XML, VALID_USAGE_POINT_ID


@pytest.fixture(autouse=True)
def _enable_custom_integrations(enable_custom_integrations: None) -> None:
    """Enable loading the custom integration for config flow tests."""
    return


async def test_form_shows(hass: HomeAssistant) -> None:
    """The initial step shows the user form with no errors."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"
    assert not result["errors"]


async def test_form_creates_entry(hass: HomeAssistant) -> None:
    """Valid ESPI XML creates a config entry."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "custom_components.green_button.async_setup_entry",
        return_value=True,
    ) as mock_setup_entry:
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {"name": "Home", "xml": VALID_ESPI_XML},
        )
        await hass.async_block_till_done()

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "Home"
    assert result["result"].unique_id == VALID_USAGE_POINT_ID
    assert len(mock_setup_entry.mock_calls) == 1


async def test_form_invalid_xml(hass: HomeAssistant) -> None:
    """Malformed XML re-shows the form with an error."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {"name": "Home", "xml": INVALID_XML},
    )

    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {"xml": "invalid_espi_xml"}


async def test_form_no_usage_points(hass: HomeAssistant) -> None:
    """A feed without a UsagePoint re-shows the form with an error."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {"name": "Home", "xml": EMPTY_FEED_XML},
    )

    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {"xml": "no_usage_points_found"}


async def test_form_already_configured(hass: HomeAssistant) -> None:
    """A UsagePoint that is already configured aborts the flow."""
    MockConfigEntry(
        domain=DOMAIN,
        unique_id=VALID_USAGE_POINT_ID,
        data={},
    ).add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {"name": "Home", "xml": VALID_ESPI_XML},
    )

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "already_configured"
