import logging
from collections import defaultdict
from datetime import datetime, timedelta
from functools import partial
from random import randint

import voluptuous as vol
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import DeviceEntry

from homeassistant.core import Config, HomeAssistant

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_REGION, CONF_ID
import homeassistant.helpers.config_validation as cv


from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.dispatcher import async_dispatcher_send
from homeassistant.helpers.event import async_call_later, async_track_time_change
from homeassistant.util import dt as dt_utils

from .const import PLATFORMS, NEW_HOUR

_LOGGER = logging.getLogger(__name__)

async def new_hr(hass, n):
    """Callback to tell the sensors to update on a new hour."""
    _LOGGER.debug("Called new_hr callback")
    async_dispatcher_send(hass, NEW_HOUR)
    
    
async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up skisporet_v2 as config entry."""
    
    for platform in PLATFORMS:
        hass.async_add_job(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )
    
    #cb_new_hr = async_track_time_change(hass, new_hr, minute=0, second=0)
    #api.listeners.append(cb_new_hr)
    
    
    #hass.config_entries.async_setup_platforms(entry, PLATFORMS)
    #entry.add_update_listener(async_reload_entry)
    return True




async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
