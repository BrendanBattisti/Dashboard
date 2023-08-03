"""
Server module for controlling lights in the house
"""
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, List

import asyncio
import json

from Modules.utils import annotate, get_datetime_int, debug_msg, Loggable
from env import LIGHTS_FILE


@dataclass
class Light:
    ip: str
    on: bool
    name: str

    def __init__(self, key, value):
        self.ip = key
        self.on = value.is_on
        self.name = value.alias

    def to_public(self):
        return PublicLight(self)


@dataclass
class PublicLight:
    on: bool
    name: str

    def __init__(self, light: Light):
        self.on = light.on
        self.name = light.name


class KasaInterface(Loggable):

    def __init__(self, light_file: str, logger) -> None:

        super().__init__(logger)
        try:
            import kasa.smartdevice
            from kasa import SmartPlug, Discover
            self.kasa = kasa
            self.SmartPlug = SmartPlug
            self.Discover = Discover
        except ImportError:
            self.active = False
        else:
            self.active = True

        self.data = {}
        self.light_file = light_file

    def require_active(self, f):

        def inner():
            if self.active:
                return f()
            return None

        return inner

    def save_lights(self) -> None:
        with open(LIGHTS_FILE, 'w') as json_file:
            json.dump(self.storage_format(), json_file, indent=2)

    def load_lights(self) -> None:
        try:
            with open(LIGHTS_FILE) as json_file:
                data = json.load(json_file)
                self.data = data['devices']

        except FileNotFoundError:
            self.data = {}

    def data_to_public_json(self) -> List[PublicLight]:
        return [device.to_public() for device in self.data]

    def storage_format(self) -> dict:
        return {'dt': get_datetime_int(), 'devices': self.data}

    @require_active
    def update_lights(self) -> None:
        self.log("Updating Lights")
        discovered_devices = asyncio.run(self.Discover.discover(target="10.0.1.255"))

        self.data = [Light(ip, device) for ip, device in discovered_devices.items()]

        self.save_lights()

    @annotate
    def send_update_lights(self) -> List[PublicLight]:
        self.update_lights()
        return self.data_to_public_json()

    @require_active
    def get_lights(self) -> List[PublicLight]:
        self.refresh_lights()
        return self.data_to_public_json()

    @annotate
    def refresh_lights(self):
        debug_msg("Refreshing lights")
        self.load_lights()

        if not self.data:
            self.update_lights()

        else:

            time_since_update = datetime.fromtimestamp(devices['dt']) - datetime.now()

            if time_since_update > timedelta(days=1):
                new_devices = update_lights()

                if len(new_devices) < len(devices):
                    return devices

                devices = new_devices

        return devices


@annotate
def format_lights(lights_data: Dict[str, kasa.smartdevice.SmartDevice]) -> list:
    formatted_lights = [None] * len(lights_data)

    for i, (k, v) in enumerate(lights_data.items()):
        new_item = {
            'ip': k,
            'on': v.is_on,
            'name': v.alias
        }

        formatted_lights[i] = new_item
    return formatted_lights


@annotate
async def kasa_new_state(device: SmartPlug, new_state: bool):
    await device.update()

    if new_state:
        await (device.turn_on())
    else:
        await (device.turn_off())


@annotate
def update_device_state(name: str, new_state: bool):
    devices = refresh_lights()['devices']

    selected = None
    selected_index = 0
    for index, device in enumerate(devices):
        if device['name'] == name:
            selected = device
            selected_index = index
            break

    if not selected:
        format_for_sending({'devices': devices})

    if selected['on'] == new_state:
        format_for_sending({'devices': devices})

    debug_msg(f"Changing {name} to {new_state}")

    # Actually change the state of the device
    real_device = SmartPlug(selected['ip'])
    try:
        asyncio.run(kasa_new_state(real_device, new_state))

    except kasa.SmartDeviceException:
        return format_for_sending({'devices': devices})
    #  Change the state of the stored device
    selected['on'] = new_state
    devices[selected_index] = selected
    save_lights(json_storage_format(devices))

    return format_for_sending({'devices': devices})
