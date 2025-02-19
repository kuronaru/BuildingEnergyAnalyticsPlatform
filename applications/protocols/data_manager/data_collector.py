import asyncio
from applications.protocols.types.bacnet_protocol import run_bacnet_configurations
from applications.database.db_bms_manager import BMSDataManager

async def collect_and_store_bacnet_data(config):
    """ 读取 BACnet 数据并存储到数据库 """
    data = await run_bacnet_configurations(config)
    if data:
        for entry in data:
            BMSDataManager.save_data(entry["object_type"], entry["object_instance"], entry["value"])
        print("Data successfully stored in database.")
    else:
        print("No data collected.")

if __name__ == "__main__":
    bacnet_config = {
        "local_ip": "10.249.156.165",
        "device_ip": "10.249.156.165",
        "local_port": 47809,
        "device_port": 63878,
        "read_objects": [("analogInput", 0), ("analogInput", 1)],
        "write_object": ("analogValue", 1, 18),  # (object_type, object_instance, value)
        "property_name": "presentValue",
        "read_attempts": 1,
        "read_interval": 1,  # reading intervals/s
        "write_interval": 5,  # wait for the value to change
        "enable_read": True,
        "enable_write": False
    }
    asyncio.run(collect_and_store_bacnet_data(bacnet_config))