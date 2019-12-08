class Image:
    def __init__(self, data, width, height):
        self.data = data
        self.width = width
        self.height = height
        self.__layers = []

    def pixelat(self, pos):
        candidates = [l[pos] for l in self.layers]
        return [c for c in candidates if c != '2'][0]

    def compose(self):
        canvas_size = self.width * self.height
        return "".join([self.pixelat(i) for i in range(canvas_size)])

    @property
    def layers(self):
        if not self.__layers:
            lsize = self.width * self.height
            partitions = range(0, len(self.data), lsize)
            self.__layers = [self.data[i:i+lsize] for i in partitions]
        return self.__layers
