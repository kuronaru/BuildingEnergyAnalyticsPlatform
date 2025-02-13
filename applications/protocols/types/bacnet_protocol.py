import BAC0
import time
import asyncio
import random

def read_values(bacnet_client, config):
    results = []
    for obj_type, obj_instance in config["read_objects"]:
        address = f"{config['device_ip']}:{config['device_port']} {obj_type} {obj_instance} {config['property_name']}"
        value = float(bacnet_client.read(address))
        results.append({"object_type": obj_type, "object_instance": obj_instance, "value": value})
        print(f"Read from {address}: {value}")
    return results


def write_value(bacnet_client, config, dynamic=False):
    obj_type, obj_instance = config["write_object"]
    if dynamic:
        set_value = random.randint(*config["write_range"])
    else:
        set_value = config["fixed_set_value"]

    write_address = f"{config['device_ip']}:{config['device_port']} {obj_type} {obj_instance} {config['property_name']}"
    bacnet_client.write(f"{write_address} {set_value}")
    print(f"Wrote {set_value} to {write_address}")
    return set_value


async def run_bacnet_configurations(config):
    try:
        bacnet_client = BAC0.lite(ip=config["local_ip"], port=config["local_port"])
        print(f"BACnet client started at {config['local_ip']}:{config['local_port']}")
        results = []

        if config["enable_read"] and not config['enable_write']:
            for _ in range(config["read_attempts"]):
                results.extend(read_values(bacnet_client, config))
                await asyncio.sleep(config["read_interval"])

        if config["enable_write"]:
            if config["dynamic_write"]:
                while True:
                    set_value = write_value(bacnet_client, config, dynamic=True)
                    await asyncio.sleep(config["write_interval"])
                    results.extend(read_values(bacnet_client, config))
            else:
                set_value = write_value(bacnet_client, config, dynamic=False)
                read_values(bacnet_client, config)

        return results
    except Exception as e:
        print(f"Error: {str(e)}")
        return []

# debug
# bacnet_config = {
#     "local_ip": '10.249.156.165',  # 使用传入的 ip 和 port
#     "device_ip": '10.249.156.165',
#     "local_port": 47809,
#     "device_port": 58503,
#     "read_objects": [("analogInput", 0)],
#     "read_attempts": 1,
#     "read_interval": 1,  # reading intervals/s
#     "write_range": (15, 25),
#     "write_object": ("analogValue", 1),  # (object_type, object_instance, value)
#     "write_interval": 3,
#     "dynamic_write": True,
#     "fixed_set_value": 18,
#     "property_name": "presentValue",
#     "enable_read": True,
#     "enable_write": True,
# }
# asyncio.run(run_bacnet_configurations(bacnet_config))
