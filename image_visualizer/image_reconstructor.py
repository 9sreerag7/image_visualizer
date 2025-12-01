import numpy as np

class ImageReconstructor:
    def __init__(self, width=225, height=225):
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
