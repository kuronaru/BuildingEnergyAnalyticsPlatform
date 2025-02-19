import BAC0
import time
import asyncio

# bacnet_config = {
#     "local_ip": "10.249.156.165",
#     "device_ip": "10.249.156.165",
#     "local_port": 47809,
#     "device_port": 63878,
#     "read_objects": [("analogInput", 0), ("analogInput", 1)],
#     "write_object": ("analogValue", 1, 22),  # (object_type, object_instance, value)
#     "property_name": "presentValue",
#     "read_attempts": 3,
#     "read_interval": 1,  # reading intervals/s
#     "write_interval": 5,  # wait for the value to change
#     "enable_read": True,
#     "enable_write": True
# }

async def read_values(bacnet_client, config):
    results = []
    for obj_type, obj_instance in config["read_objects"]:
        address = f"{config['device_ip']}:{config['device_port']} {obj_type} {obj_instance} {config['property_name']}"
        value = float(bacnet_client.read(address))
        results.append({"object_type": obj_type, "object_instance": obj_instance, "value": value})
        print(f"Read from {address}: {value}")
    return results


async def write_value(bacnet_client, config):
    obj_type, obj_instance, set_value = config["write_object"]
    write_address = f"{config['device_ip']}:{config['device_port']} {obj_type} {obj_instance} {config['property_name']}"
    bacnet_client.write(f"{write_address} {set_value}")
    print(f"Wrote {set_value} to {write_address}")
    await asyncio.sleep(config["write_interval"])


async def run_bacnet_configurations(config):
    try:
        bacnet_client = BAC0.lite(ip=config["local_ip"], port=config["local_port"])
        print(f"BACnet client started at {config['local_ip']}:{config['local_port']}")
        results = []

        if config["enable_read"]:
            for _ in range(config["read_attempts"]):
                results.extend(await read_values(bacnet_client, config))
                await asyncio.sleep(config["read_interval"])

        if config["enable_write"]:
            await write_value(bacnet_client, config)
            await asyncio.sleep(config["write_interval"])
            results.extend(await read_values(bacnet_client, config))

        return results
    except Exception as e:
        print(f"Error: {str(e)}")
        return []

# debug
# asyncio.run(run_bacnet_configurations(bacnet_config))
