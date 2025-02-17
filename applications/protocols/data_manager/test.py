import BAC0
import asyncio
import time

async def read_bacnet_value(ip, device_ip, port, device_port, object_type, object_instance, property_name):
    try:
        # 初始化 BACnet 客户端
        bacnet_client = BAC0.lite(ip=ip, port=port)
        print(f"BACnet client started at {ip}:{port}")

        for _ in range(3):
            # 读取 BACnet 设备数据
            object_instance = 0  # Temp
            address = f"{device_ip}:{device_port} {object_type} {object_instance} {property_name}"
            value1 = float(bacnet_client.read(address))
            object_instance = 1 # WATER
            address = f"{device_ip}:{device_port} {object_type} {object_instance} {property_name}"
            value2 = float(bacnet_client.read(address))

            print(f"Read IndoorTemp from {device_ip}:{port} -> {object_type} {object_instance} {property_name}: {value1}")
            print(f"Read WaterTemp from {device_ip}:{port} -> {object_type} {object_instance} {property_name}: {value2}")

            time.sleep(1)

        # change
        object_type = 'analogValue'
        object_instance = 1  # temp
        set_value = 18
        address = f"{device_ip}:{device_port} {object_type} {object_instance} {property_name}"
        bacnet_client.write(f"{address} {set_value}")


        for _ in range(3):
            object_type = 'analogInput'
            object_instance = 0  # temp
            # 读取 BACnet 设备数据
            address = f"{device_ip}:{device_port} {object_type} {object_instance} {property_name}"
            value1 = float(bacnet_client.read(address))
            object_instance = 1 # WATER
            address = f"{device_ip}:{device_port} {object_type} {object_instance} {property_name}"
            value2 = float(bacnet_client.read(address))

            print(f"Read IndoorTemp from {device_ip}:{port} -> {object_type} {object_instance} {property_name}: {value1}")
            print(f"Read WaterTemp from {device_ip}:{port} -> {object_type} {object_instance} {property_name}: {value2}")

            time.sleep(1)


        return
    except Exception as e:
        print(f"Error reading BACnet data: {str(e)}")
        return None


# 运行异步任务（兼容已有事件循环）
asyncio.run(read_bacnet_value(ip='192.168.1.22', device_ip='192.168.1.21', port=47809, device_port=51522,
                                      object_type='analogInput', object_instance=0, property_name='presentValue'))