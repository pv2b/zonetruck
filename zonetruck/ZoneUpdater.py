from zonetruck.ZoneFileUpdater import ZoneFileUpdater

def ZoneUpdater(type, **kwargs):
    if type == 'zonefile':
        return ZoneFileUpdater(**kwargs)
    else:
        raise Exception('Unknown zone updater type: %r' % type)