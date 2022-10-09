"""Support for Jellyfin sensors."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType

from .const import DATA_COORDINATORS, DOMAIN
from .coordinator import JellyfinDataT, JellyfinDataUpdateCoordinator
from .entity import JellyfinEntity


@dataclass
class JellyfinSensorEntityDescriptionMixin:
    """Mixin for required keys."""

    value_fn: Callable[[JellyfinDataT], StateType]


@dataclass
class JellyfinSensorEntityDescription(
    SensorEntityDescription, JellyfinSensorEntityDescriptionMixin
):
    """Describes Jellyfin sensor entity."""


def _count_now_playing(data: JellyfinDataT) -> int | None:
    """Count the number of now playing."""
    if data is None:
        return None

    session_ids = [
        sid for (sid, session) in data.items() if "NowPlayingItem" in session
    ]

    return len(session_ids)


SENSOR_TYPES: dict[str, JellyfinSensorEntityDescription[Any]] = {
    "sessions": JellyfinSensorEntityDescription(
        key="watching",
        icon="mdi:television-play",
        native_unit_of_measurement="Watching",
        value_fn=_count_now_playing,
    )
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Jellyfin sensor based on a config entry."""
    coordinators: dict[str, JellyfinDataUpdateCoordinator[Any]] = hass.data[DOMAIN][
        entry.entry_id
    ][DATA_COORDINATORS]

    async_add_entities(
        JellyfinSensor(coordinators[coordinator_type], description)
        for coordinator_type, description in SENSOR_TYPES.items()
    )


class JellyfinSensor(JellyfinEntity, SensorEntity):
    """Defines a Jellyfin sensor entity."""

    entity_description: JellyfinSensorEntityDescription

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        return self.entity_description.value_fn(self.coordinator.data)
