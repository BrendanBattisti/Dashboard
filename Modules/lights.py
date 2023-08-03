"""
Server module for controlling lights in the house
"""
from datetime import datetime, timedelta
from typing import Dict


import asyncio
import json


from Modules.utils import annotate, get_datetime_int, debug_msg
from env import LIGHTS_FILE


class KasaInterface:

    def __init__(self, light_file: str, logger) -> None:
        
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
            json.dump(self.data, json_file, indent=2)

    def load_lights(self) -> None:
        try:
            with open(LIGHTS_FILE) as json_file:
                data = json.load(json_file)
                self.data = json_storage_format(format_lights(data))

        except FileNotFoundError:
            self.data = {}

    @require_active
    def update_lights(self) -> None:
        debug_msg("Updating Lights")
        discovered_devices = asyncio.run(self.Discover.discover(target="10.0.1.255"))

        self.devices = json_storage_format(format_lights(discovered_devices))

        self.save_lights()


    @annotate
    def send_update_lights(self):
        self.update_lights()
        return self.format_for_sending(self.data)

    @annotate
    def get_lights(self):
        self.refresh_lights()
        return self.format_for_sending(self.data)

    def format_for_sending(self) -> list:
        return [{"name": x['name'], "on": x['on']} for x in self.data['devices']]

    @annotate
    def refresh_lights(self):
        debug_msg("Refreshing lights")
        self.load_lights()

        if not devices: self.update_lights()

        else:

            time_since_update = datetime.fromtimestamp(devices['dt']) - datetime.now()

            if time_since_update > timedelta(days=1):
                new_devices = update_lights()

                if len(new_devices) < len(devices):
                    return devices

                devices = new_devices

        return devices

    @annotate
    def json_storage_format(light_data: list) -> dict:
        return {'dt': get_datetime_int(), 'devices': light_data}

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
