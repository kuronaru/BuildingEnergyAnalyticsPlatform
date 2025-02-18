import asyncio
# from db_database_manager import save_to_database
from applications.protocols.types.bacnet_protocol import main as bacnet_main

# async def collect_data(config):
#     data = await bacnet_main(config)
#     if data:
#         save_to_database(data)