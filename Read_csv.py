# import BAC0
# import pandas as pd
# import time
# import socket
#
# # 读取 CSV
# file_path = "/mnt/data/ACMV.csv"
# df = pd.read_csv(file_path)
# columns = df.columns[1:]  # 跳过时间列
#
# # 获取本机 IP
# local_ip = socket.gethostbyname(socket.gethostname())
# port = 47808
#
# dev = BAC0.lite(ip=local_ip, port=port)
# print(f"BACnet 设备运行中，IP: {local_ip}, Port: {port}")
#
# # 创建 analogInput 对象
# for idx, col in enumerate(columns):
#     dev[('analogInput', idx)] = 0.0
#
# def send_data():
#     for _, row in df.iterrows():
#         for idx, col in enumerate(columns):
#             dev[('analogInput', idx)] = row[col]
#         print(f"已发送数据: {row[columns].to_dict()}")
#         time.sleep(15)
#
# try:
#     send_data()
# except KeyboardInterrupt:
#     print("BACnet 设备停止。")