"""
Server module for controlling lights in the house
"""
import asyncio
import dataclasses
import json
from dataclasses import dataclass
from datetime import timedelta
from typing import List
from Modules.storage import Storage

from Modules.utils import Logger, annotate, get_datetime_int, Loggable, get_time_difference


@dataclass
class Light:
    ip: str
    on: bool
    name: str

    def to_public(self):
        return PublicLight(self)


def from_kasa(ip: str, device) -> Light:
    return Light(
        ip=ip,
        on=device.is_on,
        name=device.alias
    )


@dataclass
class PublicLight:
    on: bool
    name: str

    def __init__(self, light: Light):
        self.on = light.on
        self.name = light.name


class KasaInterface(Loggable):

    def __init__(self, storage: Storage, logger: Logger) -> None:

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

        self.storage = storage
        self.recent_update = 0

    def load_lights(self) -> None:
        
        data = self.storage.get_lights()
        self.data = {k: Light(**v) for k, v in data['devices'].items()}

    def data_to_public_json(self) -> List[PublicLight]:
        return [device.to_public() for device in self.data.values()]

    def storage_format(self) -> dict:
        return {'dt': self.recent_update, 'devices': {k: dataclasses.asdict(v) for k, v in self.data.items()}}

    def update_lights(self) -> List[PublicLight]:
        if self.active:
            self.log("Updating Lights")
            discovered_devices = asyncio.run(self.Discover.discover(target="10.0.1.255"))
            self.recent_update = get_datetime_int()
            self.data = {ip: from_kasa(ip, device) for ip, device in discovered_devices.items()}
            self.storage.save_lights(self.data)
        return self.data_to_public_json()

    def get_lights(self) -> List[PublicLight]:
        self.refresh_lights()
        return self.data_to_public_json()

    @annotate
    def refresh_lights(self) -> List[PublicLight]:
        self.log("Refreshing lights")
        self.load_lights()

        if not self.data:
            self.update_lights()

        else:

            print(self.recent_update)
            time_since_update = get_time_difference(get_datetime_int())

            if time_since_update > timedelta(days=1):
                self.update_lights()

        return self.data_to_public_json()

    @annotate
    def update_device_state(self, name: str, new_state: bool):

        if self.active:
            light = None
            device_ip = None
            for ip, device in self.data.items():
                if device.name == name:
                    light = device
                    device_ip = ip
                    break

            if not light:
                return self.data_to_public_json()

            if light.on == new_state:
                return self.data_to_public_json()

            self.log(f"Changing {name} to {new_state}")

            # Actually change the state of the device
            real_device = self.SmartPlug(light.ip)
            try:
                asyncio.run(kasa_new_state(real_device, new_state))

            except self.kasa.SmartDeviceException:
                return self.data_to_public_json()
            #  Change the state of the stored device
            light.on = new_state
            self.data[device_ip] = light
            self.save_lights()

        return self.data_to_public_json()


async def kasa_new_state(device, new_state: bool) -> None:
    await device.update()

    if new_state:
        await (device.turn_on())
    else:
        await (device.turn_off())
