class ZoneFilter:
    def __init__(self, rules):
        self.rules = rules
    def filter(self, record):
        # TODO Dummy implementation
        return [record]