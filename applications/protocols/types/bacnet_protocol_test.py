import BAC0
import asyncio
import random
import time

# Config
config = {
    "local_ip": "10.249.156.165",
    "device_ip": "10.249.156.165",
    "local_port": 47809,
    "device_port": 59450,
    "read_objects": [("analogInput", 0), ("analogInput", 1)],
    "read_attempts": 3,
    "read_interval": 60,  # reading intervals/s

    "write_range": (15, 25),
    "write_object": ("analogValue", 1),  # (object_type, object_instance, value)
    "write_interval": 3,
    "dynamic_write": True,
    "fixed_set_value": 18,


    "property_name": "presentValue",
    "enable_read": True,
    "enable_write": False,
}


def read_values(bacnet_client):
    for obj_type, obj_instance in config["read_objects"]:
        address = f"{config['device_ip']}:{config['device_port']} {obj_type} {obj_instance} {config['property_name']}"
        value = float(bacnet_client.read(address))
        print(f"Read from {address}: {value}")


def write_value(bacnet_client, dynamic=False):
    obj_type, obj_instance = config["write_object"]
    if dynamic:
        set_value = random.randint(*config["write_range"])
    else:
        set_value = config["fixed_set_value"]

    write_address = f"{config['device_ip']}:{config['device_port']} {obj_type} {obj_instance} {config['property_name']}"
    bacnet_client.write(f"{write_address} {set_value}")
    print(f"Wrote {set_value} to {write_address}")
    return set_value


async def main():
    try:
        bacnet_client = BAC0.lite(ip=config["local_ip"], port=config["local_port"])
        print(f"BACnet client started at {config['local_ip']}:{config['local_port']}")

        # If only reading is enabled
        if config["enable_read"] and not config["enable_write"]:
            while True:  # Infinite loop for continuous reading
                read_values(bacnet_client)
                await asyncio.sleep(config["read_interval"])  # 1s interval between reads

        # If writing is enabled
        if config["enable_write"]:
            if config["dynamic_write"]:
                while True:  # Dynamic write: Keep writing random values until condition is met
                    set_value = write_value(bacnet_client, dynamic=True)

                    # Read after writing
                    read_values(bacnet_client)

                    await asyncio.sleep(config["write_interval"])  # Wait before next write

            else:
                set_value = write_value(bacnet_client, dynamic=False)  # Write a fixed value
                read_values(bacnet_client)  # Read after writing

    except Exception as e:
        print(f"Error: {str(e)}")

# Run the task
asyncio.run(main())
