"""Text entities."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.text import TextEntity

from .entity import HCEntity
from .helpers import create_entities, error_decorator

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from . import HCConfigEntry
    from .entity_descriptions.descriptions_definitions import HCTextEntityDescription

PARALLEL_UPDATES = 0


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001
    config_entry: HCConfigEntry,
    async_add_entites: AddEntitiesCallback,
) -> None:
    """Set up text platform."""
    entities = create_entities({"text": HCText}, config_entry.runtime_data)
    async_add_entites(entities)


class HCText(HCEntity, TextEntity):
    """Text Entity."""

    entity_description: HCTextEntityDescription

    @property
    def native_value(self) -> str | None:
        if self._entity.value is None:
            return None
        return str(self._entity.value)

    @property
    def native_max(self) -> int:
        if hasattr(self._entity, "max") and self._entity.max is not None:
            return int(self._entity.max)
        return self.entity_description.native_max

    @error_decorator
    async def async_set_value(self, value: str) -> None:
        await self._entity.set_value(value)
