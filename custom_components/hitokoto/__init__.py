from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN, PLATFORMS
from .config_flow import HitokotoOptionsFlowHandler

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Hitokoto from a config entry."""
    if not entry.options:
        hass.config_entries.async_update_entry(
            entry,
            options={"category": "k", "update_interval": 3600}
        )

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

def async_get_options_flow(config_entry):
    """获取选项流."""
    return HitokotoOptionsFlowHandler(config_entry)
