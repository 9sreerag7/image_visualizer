def parse_ccsds_header(packet):
    """
    Simple CCSDS parser (primary header only)
    CCSDS primary header: 6 bytes
    - 2 bytes: Packet ID
    - 2 bytes: Sequence Control
    - 2 bytes: Packet Length
    The rest: Payload
    """
    if len(packet) < 6:
        return None  # invalid packet

    packet_id = int.from_bytes(packet[0:2], byteorder='big')
    seq_ctrl = int.from_bytes(packet[2:4], byteorder='big')
    pkt_len = int.from_bytes(packet[4:6], byteorder='big')
    payload = packet[6:]

    return {
        "packet_id": packet_id,
        "sequence": seq_ctrl,
        "length": pkt_len,
        "payload": payload
    }
