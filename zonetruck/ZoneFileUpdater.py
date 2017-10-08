class ZoneFileUpdater: # pylint: disable=too-few-public-methods
    def __init__(self, path):
        self.path = path
    def task(self, zone):
        with open(self.path, 'w') as file:
            names = zone.nodes.keys()
            for name in names:
                print(zone[name].to_text(name), file=file)