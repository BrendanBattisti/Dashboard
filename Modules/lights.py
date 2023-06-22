"""
Server module for controlling lights in the house
"""
from datetime import datetime, timedelta
from typing import Dict

import kasa.smartdevice
from kasa import SmartPlug, Discover
import asyncio
import json

from Modules.utils import get_datetime_int, debug_msg

data_file = "light_data.json"
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def save_lights(data):
    with open(data_file, 'w') as json_file:
        json.dump(data, json_file, indent=2)


def load_lights():
    try:
        with open(data_file) as json_file:
            return json.load(json_file)

    except FileNotFoundError:
        return {}


def update_lights():
    debug_msg("Updating Lights")
    discovered_devices = asyncio.run(Discover.discover(target="10.0.1.255"))

    devices = json_storage_format(format_lights(discovered_devices))

    save_lights(devices)

    return devices


def send_update_lights():
    return format_for_sending(update_lights())


def get_lights():
    return format_for_sending(refresh_lights())


def format_for_sending(devices: dict) -> list:
    return [{"name": x['name'], "on": x['on']} for x in devices['devices']]


def refresh_lights():
    debug_msg("Refreshing lights")
    devices = load_lights()

    if not devices:
        devices = update_lights()

    else:

        time_since_update = datetime.fromtimestamp(devices['dt']) - datetime.now()

        if time_since_update > timedelta(days=1):
            new_devices = update_lights()

            if len(new_devices) < len(devices):
                return devices

            devices = new_devices

    return devices


def json_storage_format(light_data: list) -> dict:
    return {'dt': get_datetime_int(), 'devices': light_data}


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


async def kasa_new_state(device: SmartPlug, new_state: bool):
    await device.update()

    if new_state:
        await (device.turn_on())
    else:
        await (device.turn_off())


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
