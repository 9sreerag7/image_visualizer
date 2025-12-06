'''import numpy as np

class ImageReconstructor:
    def __init__(self, width=6000, height=4000):
        self.buffer = bytearray()
        self.width = width
        self.height = height
        self.total_size = self.width * self.height

    def add_data(self, data):
        self.buffer.extend(data)

    def get_image(self):
        if len(self.buffer) >= self.total_size:
            arr = np.frombuffer(self.buffer[:self.total_size], dtype=np.uint8)
            return arr.reshape((self.height, self.width))
        return None

    def reset(self):
        self.buffer = bytearray()
'''




# image_reconstructor.py
import numpy as np

class ImageReconstructor:
    def __init__(self):
        self.width = None
        self.height = None
        self.total_bytes = None
        self.total_chunks = None
        self.chunk_size = None  # payload size per chunk (sender and receiver must agree on this nominal value)
        self.buffer = None      # bytearray of total_bytes
        self.received_chunks = set()

    def setup(self, width, height, total_bytes, total_chunks, chunk_size):
        self.width = width
        self.height = height
        self.total_bytes = total_bytes
        self.total_chunks = total_chunks
        self.chunk_size = chunk_size
        self.buffer = bytearray(b'\x00') * total_bytes
        self.received_chunks = set()

    def add_chunk(self, chunk_index, payload):
        if self.buffer is None:
            raise RuntimeError("Reconstructor not initialized")

        start = chunk_index * self.chunk_size
        end = start + len(payload)
        # Clip end so we don't write past buffer (safety)
        if start >= self.total_bytes:
            return False

        if end > self.total_bytes:
            end = self.total_bytes

        self.buffer[start:end] = payload[: end - start ]
        self.received_chunks.add(chunk_index)
        return True

    def progress(self):
        if self.total_chunks is None:
            return 0.0
        return len(self.received_chunks) / self.total_chunks

    def is_complete(self):
        return (self.total_chunks is not None) and (len(self.received_chunks) >= self.total_chunks)

    def get_image(self):
        if self.buffer is None:
            return None
        if self.width is None or self.height is None:
            return None
        # Return an ndarray view into buffer
        arr = np.frombuffer(self.buffer, dtype=np.uint8)
        try:
            return arr.reshape((self.height, self.width))
        except Exception:
            return None

    def reset(self):
        self.__init__()
