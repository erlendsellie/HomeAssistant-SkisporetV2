"""Config flow for Skisporet V2 integration."""
import logging

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_ID, CONF_PASSWORD, CONF_USERNAME

from .const import DOMAIN, SEGMENT_ID, NAME

_LOGGER = logging.getLogger(__name__)


class SkisporetV2ConfigFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Skisporet V2."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    async def _show_setup_form(self, errors=None):
        """Show the setup form to the user."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {vol.Required(NAME): str, vol.Required(SEGMENT_ID): str}
            ),
            errors=errors or {},
        )

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is None:
            return await self._show_setup_form()

        title = DOMAIN + ' ' + user_input[NAME]
        title = DOMAIN
        return self.async_create_entry(
            title=title,
            data=user_input,
        )
