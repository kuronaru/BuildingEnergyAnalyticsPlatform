import pandas as pd
import re

# import and read the data
file_path = "BAcnet ID.xlsx"
df = pd.read_excel(file_path, usecols=[1])  # read the second column


# processing
def parse_bacnet_id(bacnet_str):
    """ Parse BACnet ID（'AI:3001181' = ('analogInput', 3001181)） """
    match = re.match(r"([A-Z]+):(\d+)", str(bacnet_str))
    if match:
        obj_type, obj_instance = match.groups()
        type_map = {
            "AI": "analogInput",
            "AV": "analogValue",
            "BI": "binaryInput",
            "BV": "binaryValue"}
        return type_map.get(obj_type, obj_type), int(obj_instance)
    return None, None


# extract instance number
df[['Object Type', 'Instance Number']] = df.iloc[:, 0].apply(lambda x: pd.Series(parse_bacnet_id(x)))

# check the result id
bacnet_id_list = df[['Object Type', 'Instance Number']].dropna().values.tolist()
# print("BACnet ID list：", bacnet_id_list)

# separate AI and AV as read and write objects
bacnet_read_list = bacnet_id_list[:-5]
# print("BACnet read list：", bacnet_read_list)
bacnet_write_list = bacnet_id_list[-5:]
# print("BACnet write list：", bacnet_write_list[1])

# configuration list
bacnet_config = {
    "local_ip": "10.249.156.165",
    "device_ip": "10.249.156.165",
    "local_port": 47809,
    "device_port": 58503,
    "read_objects": bacnet_read_list,
    "read_attempts": 1,
    "read_interval": 1,  # reading intervals/s

    "write_range": (15, 25),
    "write_object": bacnet_write_list[1],  # choose the object to write
    "write_interval": 3,    # writing intervals/s
    "dynamic_write": True,
    "fixed_set_value": 18,

    "property_name": "presentValue",
    "enable_read": True,
    "enable_write": False,
}
