from applications.protocols.protocols.modbus_protocol import ModbusProtocol
from applications.protocols.protocols.bacnet_protocol import BACnetProtocol

class ProtocolFactory:
    @staticmethod
    def create_protocol(protocol_type, **kwargs):

        if protocol_type == "Modbus":
            return ModbusProtocol(**kwargs)
        elif protocol_type == "BACnet":
            return BACnetProtocol(**kwargs)

        # other protocols can be added

        else:
            raise ValueError(f"Unsupported protocol type: {protocol_type}")
