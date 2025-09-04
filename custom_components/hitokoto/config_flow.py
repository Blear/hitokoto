from homeassistant import config_entries
import voluptuous as vol
from .const import DOMAIN

CATEGORIES = {
    "a": "动画", "b": "漫画", "c": "游戏", "d": "文学", "e": "原创",
    "f": "来自网络", "g": "其他", "h": "影视", "i": "诗词",
    "j": "网易云", "k": "哲学", "l": "抖机灵"
}

UPDATE_INTERVALS = {
    300: "5分钟",
    900: "15分钟",
    1800: "30分钟",
    3600: "1小时",
    7200: "2小时",
    21600: "6小时",
    43200: "12小时",
    86400: "1天"
}


class HitokotoConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Hitokoto 配置流."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(
                title="Hitokoto 每日一言",
                data={},
                options=user_input
            )

        schema = vol.Schema({
            vol.Optional("category", default="k"): vol.In(CATEGORIES),
            vol.Optional("update_interval", default=3600): vol.In(UPDATE_INTERVALS),
        })

        return self.async_show_form(step_id="user", data_schema=schema)


class HitokotoOptionsFlowHandler(config_entries.OptionsFlow):
    """Options Flow 允许修改配置"""

    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        current = self.config_entry.options or {}
        schema = vol.Schema({
            vol.Optional("category", default=current.get("category", "k")): vol.In(CATEGORIES),
            vol.Optional("update_interval", default=current.get("update_interval", 3600)): vol.In(UPDATE_INTERVALS),
        })

        return self.async_show_form(step_id="init", data_schema=schema)
