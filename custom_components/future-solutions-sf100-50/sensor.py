"""Support for Future Solutions SF100-50 sensors."""
from __future__ import annotations

from homeassistant import config_entries
from homeassistant.components.bluetooth.passive_update_processor import (
    PassiveBluetoothDataProcessor,
    PassiveBluetoothDataUpdate,
    PassiveBluetoothEntityKey,
    PassiveBluetoothProcessorCoordinator,
    PassiveBluetoothProcessorEntity,
)
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import (
    UnitOfTemperature,
    UnitOfPower,
    UnitOfElectricCurrent,
    UnitOfElectricPotential
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.sensor import sensor_device_info_to_hass_device_info

from .const import DOMAIN

SENSOR_DESCRIPTIONS = {
    "solar_charger_pv_voltage": SensorEntityDescription(
        key="solar_charger_pv_voltage",
        device_class = SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement = UnitOfElectricPotential.VOLT,
        state_class = SensorStateClass.MEASUREMENT,
    ),
    "solar_charger_output_power": SensorEntityDescription(
        key="solar_charger_output_power",
        device_class = SensorDeviceClass.POWER,
        native_unit_of_measurement = UnitOfPower.WATT,
        state_class = SensorStateClass.MEASUREMENT,
    ),
    "solar_charger_energy_harvest_today": SensorEntityDescription(
        key="solar_charger_energy_harvest_today",
        device_class = SensorDeviceClass.POWER,
        native_unit_of_measurement = UnitOfPower.KILO_WATT,
        state_class = SensorStateClass.TOTAL_INCREASING,
    ),
    "solar_charger_internal_temparature": SensorEntityDescription(
        key="solar_charger_internal_temperature",
        device_class = SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement = UnitOfTemperature.CELSIUS,
        state_class = SensorStateClass.MEASUREMENT,
    ),
    "battery_current": SensorEntityDescription(
        key="battery_current",
        device_class = SensorDeviceClass.CURRENT,
        native_unit_of_measurement = UnitOfElectricCurrent.AMPERE,
        state_class = SensorStateClass.MEASUREMENT,
    ),
    "battery_voltage": SensorEntityDescription(
        key="battery_voltage",
        device_class = SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement = UnitOfElectricPotential.VOLT,
        state_class = SensorStateClass.MEASUREMENT,
    ),
}

### Example Code
# def sensor_update_to_bluetooth_data_update(parsed_data):
#     """Convert a sensor update to a Bluetooth data update."""
#     # This function must convert the parsed_data
#     # from your library's update_method to a `PassiveBluetoothDataUpdate`
#     # See the structure above
#     return PassiveBluetoothDataUpdate(
#         devices={},
#         entity_descriptions={},
#         entity_data={},
#         entity_names={},
#     )
### Example Code

async def async_setup_entry(
    hass: HomeAssistant,
    entry: config_entries.ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the SF100-50 BLE sensors."""
    coordinator: PassiveBluetoothProcessorCoordinator = hass.data[DOMAIN][
        entry.entry_id
    ]
    processor = PassiveBluetoothDataProcessor(sensor_update_to_bluetooth_data_update)
    entry.async_on_unload(
        processor.async_add_entities_listener(
            MopekaBluetoothSensorEntity, async_add_entities
        )
    )
    entry.async_on_unload(coordinator.async_register_processor(processor))


class SF100_50BluetoothSensorEntity(PassiveBluetoothProcessorEntity, SensorEntity):
    """Representation of an SF100-50 BLE sensor."""

    @property
    def native_value(self) -> float | int | str | None:
        """Return the native value."""
        return self.processor.entity_data.get(self.entity_key)