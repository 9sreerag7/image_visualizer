'''def parse_ccsds_header(packet):
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
    }'''





# ccsds_header_parser.py
def parse_ccsds_header(packet):
    """
    Packet layout we use:
    [0:6]   - fake CCSDS primary header (6 bytes)
    [6:10]  - width (4 bytes, big-endian uint32)
    [10:14] - height (4 bytes, big-endian uint32)
    [14:22] - total_bytes (8 bytes, big-endian uint64)
    [22:26] - chunk_index (4 bytes, big-endian uint32)
    [26:30] - total_chunks (4 bytes, big-endian uint32)
    [30:]   - payload bytes for this chunk
    """
    if len(packet) < 30:
        return None

    try:
        packet_id = int.from_bytes(packet[0:2], 'big')
        seq = int.from_bytes(packet[2:4], 'big')
        pkt_len = int.from_bytes(packet[4:6], 'big')

        width = int.from_bytes(packet[6:10], 'big')
        height = int.from_bytes(packet[10:14], 'big')
        total_bytes = int.from_bytes(packet[14:22], 'big')
        chunk_index = int.from_bytes(packet[22:26], 'big')
        total_chunks = int.from_bytes(packet[26:30], 'big')

        payload = packet[30:]
    except Exception:
        return None

    return {
        "packet_id": packet_id,
        "seq": seq,
        "pkt_len": pkt_len,
        "width": width,
        "height": height,
        "total_bytes": total_bytes,
        "chunk_index": chunk_index,
        "total_chunks": total_chunks,
        "payload": payload
    }
