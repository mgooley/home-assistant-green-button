"""Config flow for Green Button integration."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult

from . import configs, const, state

_LOGGER = logging.getLogger(__name__)


class GreenButtonConfigFlow(ConfigFlow, domain=const.DOMAIN):
    """Handle a config flow for Green Button."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        await state.async_ensure_setup(self.hass)

        step_id = "user"
        schema = configs.ComponentConfig.make_config_entry_step_schema(user_input)
        if user_input is None:
            return self.async_show_form(
                step_id=step_id,
                data_schema=schema,
            )

        try:
            config = configs.ComponentConfig.from_mapping(user_input)
        except configs.InvalidUserInputError as ex:
            _LOGGER.debug("Invalid user input", exc_info=True)
            return self.async_show_form(
                step_id=step_id,
                data_schema=schema,
                errors=ex.errors,
            )

        await self.async_set_unique_id(config.unique_id)
        self._abort_if_unique_id_configured()

        _LOGGER.debug("Created config with unique ID %r", config.unique_id)
        config.set_side_channels(self.hass)
        return self.async_create_entry(
            title=config.name,
            data=config.to_mapping(),
        )
