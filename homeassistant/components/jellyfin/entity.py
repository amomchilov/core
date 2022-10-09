"""Base Entity for Jellyfin."""
from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers.entity import DeviceInfo, EntityDescription
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DEFAULT_NAME, DOMAIN
from .coordinator import JellyfinDataT, JellyfinDataUpdateCoordinator


class JellyfinEntity(CoordinatorEntity[JellyfinDataUpdateCoordinator[JellyfinDataT]]):
    """Defines a base Jellyfin entity."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: JellyfinDataUpdateCoordinator[JellyfinDataT],
        description: EntityDescription,
    ) -> None:
        """Initialize the Jellyfin entity."""
        super().__init__(coordinator)
        self.coordinator = coordinator
        self.entity_description = description
        self._attr_unique_id = f"{coordinator.server_id}_{description.key}"

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information about the application."""
        return DeviceInfo(
            entry_type=DeviceEntryType.SERVICE,
            identifiers={(DOMAIN, self.coordinator.server_id)},
            manufacturer=DEFAULT_NAME,
            name=self.coordinator.server_name,
            sw_version=self.coordinator.server_version,
        )
