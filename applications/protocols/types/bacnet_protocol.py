import BAC0
import asyncio
import time

# Config
BACnet_CONFIG = {
    "local_ip": "10.249.156.165",
    "device_ip": "10.249.156.165",
    "local_port": 47809,
    "device_port": 60099,
    "read_objects": [("analogInput", 0), ("analogInput", 1)],
    "write_object": ("analogValue", 1, 18),  # (object_type, object_instance, value)
    "property_name": "presentValue",
    "read_attempts": 3,
    "read_interval": 1,  # reading intervals/s
    "write_interval": 5,  # wait for the value to change
    "enable_read": False,
    "enable_write": False
}


def read_values(bacnet_client):
    for obj_type, obj_instance in BACnet_CONFIG["read_objects"]:
        address = f"{BACnet_CONFIG['device_ip']}:{BACnet_CONFIG['device_port']} {obj_type} {obj_instance} {BACnet_CONFIG['property_name']}"
        value = float(bacnet_client.read(address))
        print(f"Read from {address}: {value}")


def write_value(bacnet_client):
    obj_type, obj_instance, set_value = BACnet_CONFIG["write_object"]
    write_address = f"{BACnet_CONFIG['device_ip']}:{BACnet_CONFIG['device_port']} {obj_type} {obj_instance} {BACnet_CONFIG['property_name']}"
    bacnet_client.write(f"{write_address} {set_value}")
    print(f"Wrote {set_value} to {write_address}")


async def main():
    try:
        bacnet_client = BAC0.lite(ip=BACnet_CONFIG["local_ip"], port=BACnet_CONFIG["local_port"])
        print(f"BACnet client started at {BACnet_CONFIG['local_ip']}:{BACnet_CONFIG['local_port']}")

        if BACnet_CONFIG["enable_read"]:
            for _ in range(BACnet_CONFIG["read_attempts"]):
                read_values(bacnet_client)
                time.sleep(BACnet_CONFIG["read_interval"])

        if BACnet_CONFIG["enable_write"]:
            write_value(bacnet_client)
            time.sleep(BACnet_CONFIG["write_interval"])
            read_values(bacnet_client)
    except Exception as e:
        print(f"Error: {str(e)}")


# Run the task
asyncio.run(main())
