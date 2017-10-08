from work_manager import WorkManager

def main():
    # TODO Parse the command line

    # TODO Parse the configuration file
    # Construct objects for:
    #   Source zone downloader object
    #   Filter objects
    #   Target zone updater objects

    # zones
    # filters
    # updaters
    

    # TODO Create a set of workers and a priority queue.
    # Each object on a priority queue should be on the following format:
    # (priority, task1, [[task2], [task3, task4]])
    # Where:
    #   The first element of the tuple, priority,  is an integer indicating the
    #   priority (lower numbers are processed first) of the task to be performed
    #   The second element of the tuple, task1, is a function to be called. It
    #   it called with no arguments, any such arguments are to be curried in.
    #   The third element is a list of subsequent task lists. After executing
    #   task1, the worker should place new objects on the task queue,
    #   corresponding to the every member of the first object of the task list.

    subsequentTasks = [[lambda zone:filter_zone(zone, filters)],
                       [lambda zone:zone_updater.update_zone(zone)
                        for zone_updater in zone_updaters]]
    
    wm = WorkManager()
    for zone in zones:
        wm.submitWork(100, lambda:xfer_zone(zone), subsequentTasks)

    wm.join()
