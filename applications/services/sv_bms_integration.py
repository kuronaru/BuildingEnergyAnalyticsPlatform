import asyncio
from applications.protocols.types.bacnet_protocol import main as bacnet_main

def run_bacnet_service(config):
    """服务器调用BACnet运行"""
    return asyncio.run(bacnet_main(config))