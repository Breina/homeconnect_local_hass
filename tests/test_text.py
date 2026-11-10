"""Tests for text entity."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.text import ATTR_MAX, ATTR_VALUE, SERVICE_SET_VALUE
from homeassistant.components.text import DOMAIN as TEXT_DOMAIN
from homeassistant.const import ATTR_ENTITY_ID, ATTR_FRIENDLY_NAME, STATE_UNKNOWN
from homeconnect_websocket.message import Action, Message

from . import setup_config_entry
from .const import CONFIG_ENTRIES

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeconnect_websocket.testutils import MockAppliance

ENTITY_ID = "text.fake_brand_homeappliance_text"


async def test_setup(
    hass: HomeAssistant,
    mock_appliance: MockAppliance,
    patch_entity_description: None,
) -> None:
    """Test setting up entity."""
    assert await setup_config_entry(hass, CONFIG_ENTRIES[0])

    state = hass.states.get(ENTITY_ID)
    assert state
    assert state.name == "Fake_brand HomeAppliance Text"
    assert state.attributes[ATTR_FRIENDLY_NAME] == "Fake_brand HomeAppliance Text"
    assert state.attributes[ATTR_MAX] == 16
    assert state.state == STATE_UNKNOWN


async def test_update(
    hass: HomeAssistant,
    mock_appliance: MockAppliance,
    patch_entity_description: None,
) -> None:
    """Test updating entity."""
    assert await setup_config_entry(hass, CONFIG_ENTRIES[0])

    await mock_appliance.entities["Test.Text"].update({"value": "Eco 40-60"})
    await hass.async_block_till_done()
    assert hass.states.get(ENTITY_ID).state == "Eco 40-60"


async def test_set(
    hass: HomeAssistant,
    mock_appliance: MockAppliance,
    patch_entity_description: None,
) -> None:
    """Test setting the value."""
    assert await setup_config_entry(hass, CONFIG_ENTRIES[0])

    await hass.services.async_call(
        TEXT_DOMAIN,
        SERVICE_SET_VALUE,
        {ATTR_ENTITY_ID: ENTITY_ID, ATTR_VALUE: "Cotton"},
        blocking=True,
    )
    mock_appliance.session.send_sync.assert_awaited_once_with(
        Message(
            resource="/ro/values",
            action=Action.POST,
            data={"uid": 205, "value": "Cotton"},
        )
    )
