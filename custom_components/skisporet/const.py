from homeassistant.components.sensor import PLATFORM_SCHEMA
import voluptuous as vol
import homeassistant.helpers.config_validation as cv



SEGMENT_ID = 'segment_id'
NAME = 'name'
DOMAIN = 'skisporet_v2'
NEW_HOUR = 'new_hour'

PLATFORMS = [
    "sensor",
]


PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(NAME): cv.string,
        vol.Required(SEGMENT_ID): cv.positive_int,
    },
    extra=vol.ALLOW_EXTRA,
)
