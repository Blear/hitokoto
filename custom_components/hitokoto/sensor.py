from datetime import timedelta
import aiohttp
import async_timeout
import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    """Set up Hitokoto sensor from config entry."""
    coordinator = HitokotoCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()
    async_add_entities([HitokotoSensor(coordinator, entry)])

    # 监听配置变化
    entry.async_on_unload(
        entry.add_update_listener(_async_update_listener)
    )


async def _async_update_listener(hass: HomeAssistant, entry: ConfigEntry):
    """处理配置更新."""
    await hass.config_entries.async_reload(entry.entry_id)


class HitokotoCoordinator(DataUpdateCoordinator):
    """Hitokoto 数据协调器."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry):
        self.entry = entry
        
        # 直接使用秒作为单位
        update_interval = timedelta(
            seconds=int(entry.options.get("update_interval", 3600))
        )

        super().__init__(
            hass,
            _LOGGER,
            name="Hitokoto 每日一言",
            update_method=self._async_fetch,
            update_interval=update_interval,
        )

    async def _async_fetch(self):
        """获取数据."""
        category = self.entry.options.get("category", "k")
        url = f"https://v1.hitokoto.cn/?c={category}&min_length=20"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with async_timeout.timeout(10):
                    async with session.get(url) as resp:
                        if resp.status != 200:
                            raise UpdateFailed(f"API 返回错误: {resp.status}")
                        data = await resp.json()
                        
                        # 确保有基础数据
                        if not data.get("hitokoto"):
                            data["hitokoto"] = "加载中..."
                        return data
                        
        except Exception as err:
            # 返回占位数据，避免实体完全不可用
            _LOGGER.warning(f"首次获取数据失败，使用占位数据: {err}")
            return {
                "hitokoto": "加载失败，请检查网络连接",
                "from": "系统提示",
                "from_who": "Hitokoto集成",
                "type": "error",
                "creator": "system",
                "uuid": "error-placeholder"
            }


class HitokotoSensor(SensorEntity):
    """Hitokoto 传感器."""

    def __init__(self, coordinator: HitokotoCoordinator, entry: ConfigEntry):
        self.coordinator = coordinator
        self._attr_unique_id = f"{DOMAIN}_{entry.entry_id}"
        self._attr_name = "Hitokoto 一言"

    @property
    def native_value(self):
        """返回当前值."""
        return self.coordinator.data.get("hitokoto") if self.coordinator.data else None

    @property
    def extra_state_attributes(self):
        """返回额外属性."""
        data = self.coordinator.data or {}
        return {
            "from": data.get("from"),
            "from_who": data.get("from_who") or "佚名",
            "type": data.get("type"),
            "creator": data.get("creator"),
            "uuid": data.get("uuid"),
        }

    @property
    def should_poll(self):
        """不需要轮询，使用协调器."""
        return False

    @property
    def available(self):
        """是否可用 - 即使有错误数据也显示为可用，让用户看到错误信息"""
        return True

    async def async_added_to_hass(self):
        """当实体添加到Home Assistant时."""
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )
