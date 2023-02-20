import logging
import requests
import voluptuous as vol

from homeassistant.const import CONF_NAME, CONF_SCAN_INTERVAL
from .const import DOMAIN, NEW_HOUR
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.dispatcher import async_dispatcher_connect, async_dispatcher_send
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)

import datetime

import logging
import asyncio
import socket
from typing import Optional
import aiohttp
import async_timeout

from .const import SEGMENT_ID, NAME, DOMAIN

_LOGGER = logging.getLogger(__name__)
TIMEOUT = 10

HEADERS = {"content-type": "application/json; charset=UTF-8", "x-requested-with": "XMLHttpRequest"}


    
async def async_setup_entry(hass, config, async_add_devices):
    data = config.data
    name = data.get(NAME)
    segment_id = data.get(SEGMENT_ID)

    async_add_devices(
        [
            Skisporet(hass, name, segment_id, config.entry_id),
        ],
        True,
    )

class Skisporet(SensorEntity):
    """Representation of a sensor that fetches data from a JSON API."""

    def __init__(self,hass, name, segment_id, unique_id):
        """Initialize the JSON API sensor."""
        self._hass = hass
        self._name = name
        self._scan_interval = 60*10
        self._state = None
        self._days = None
        self._hours = None
        self._state_raw = None
        self._just_prepped = None
        self._segment_id = segment_id

    @property
    def name(self):
        """Return the name of the sensor."""
        return DOMAIN + '_' + self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    async def fetch_data(self):
        """Fetch new state data for the sensor."""
        try:
            url =f"https://skisporet.no/map/segment/{self._segment_id}?_data=routes%2Fmap%2Fsegment.%24segmentId"
            response = await self._hass.async_add_executor_job(self.fetch,url)
            if response.status_code != 200:
                return
            data = response.json()
            if('segment' in data):
                segment = data.get('segment')
                newestPrep = segment.get('newestPrep')
                hours = newestPrep.get('hours')
                days = newestPrep.get('days')
                
                self._hours = hours
                
                if(days is not None):
                    hours = hours + (days * 24)                
                    
                now = datetime.datetime.now()
                
                state_raw = now - datetime.timedelta(hours=hours)
                state_nice = now - datetime.timedelta(hours=hours, minutes=now.minute, seconds=now.second, microseconds=now.microsecond)
                
                self._days = days
                self._just_prepped = hours < 3
                self._state_raw = state_raw
                self._state = state_nice
                
        except requests.exceptions.RequestException as error:
            _LOGGER.error("Error fetching data: %s", error)
            
    def fetch(self, url):
        return requests.get(url)

        
    def update_sensor(self):
        self.async_write_ha_state()
        
    async def new_hour(self):
        #self.update_sensor()
        await self.fetch_data()
        self.async_write_ha_state()
        

    async def async_added_to_hass(self):
        """Connect to dispatcher listening for entity data notifications."""
        await self.fetch_data()
        await super().async_added_to_hass()
        async_dispatcher_connect(self._hass, NEW_HOUR, self.new_hour)

    @property
    def extra_state_attributes(self) -> dict:
        return {
            "days": self._days,
            "hours": self._hours,
            #"nice": self._state_raw,
            "just_prepped": self._just_prepped,
            "segment_id": self._segment_id,
            "url": f"https://skisporet.no/map/segment/{self._segment_id}"

        }
        

    @property
    def device_class(self):
        return 'timestamp'
    
    
    @property
    def icon(self) -> str:
        return "mdi:ski"


    @property
    def device_name(self) -> str:
        return DOMAIN + self._name

    @property
    def device_unique_id(self):
        name = "%s_%s_%s" % (
            DOMAIN,
            self._name,
            self._segment_id,
        )
        name = name.lower().replace(".", "")
        return name

    @property
    def device_info(self):
        return DeviceInfo(
            identifiers={(DOMAIN, self.device_unique_id)},
            name=self.device_name,
            manufacturer=DOMAIN,
        )        