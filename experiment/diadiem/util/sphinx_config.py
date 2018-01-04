class SphinxConfig:
    def __init__(self):
        self.lines = []
        self.file = None

    def read(self, file):
        self.file = file
        self.lines = open(file).read().splitlines()

    def save(self):
        content = "\n".join(self.lines)
        open(self.file, "w").write(content)

    def set(self, key, value):
        for i, line in enumerate(self.lines):
            if line.startswith(key):
                content = "{} = {};".format(key, value)
                self.lines[i] = content
        self.save()

