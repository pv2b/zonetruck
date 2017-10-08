import yaml
from zonetruck.WorkManager import WorkManager
from zonetruck.ZoneUpdater import ZoneUpdater
from zonetruck.ZoneFilter import ZoneFilter
from zonetruck.zone_xfer import zone_xfer
import sys

def main(argv=None):
    argv = argv or sys.argv
    config = yaml.safe_load(open(argv[1], 'r'))

    zone_filter = ZoneFilter(config['filter_rules']).filter
    zone_updaters = [ZoneUpdater(**o).task for o in config['outputs']]

    subsequent_tasks = [[zone_filter], zone_updaters]

    work_manager = WorkManager()

    for source in config['sources']:
        for zone in source['zones']:
            work_manager.submit_work(100, zone_xfer, (source['masters'], zone), subsequent_tasks)

    work_manager.start()
    work_manager.join()

if __name__ == '__main__':
    main()