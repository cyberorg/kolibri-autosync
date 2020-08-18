#!/usr/bin/python3
# MSS Cloud sync for primary facility on user device
def run_sync():
    import os
    import sys
    import threading
    f = open(os.devnull, 'w')
    sys.stdout = f
    import logging
    logging.disable(logging.INFO)
    logging.disable(logging.WARNING)
    from kolibri.utils.cli import main
    from configparser import ConfigParser
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

    from kolibri.core.auth.models import Facility

    KOLIBRI_HOME = os.environ.get("KOLIBRI_HOME")
    syncini_file = os.path.join(KOLIBRI_HOME, "syncoptions.ini")
    configur = ConfigParser()

    try:
        file = open(syncini_file, 'r')
    except IOError:
        configur['DEFAULT'] = { 'SYNC_ON': 'True',
                                'SYNC_SERVER': 'content.myscoolserver.in',
                                'SYNC_USER': 'syncuser',
                                'SYNC_DELAY': '900.0'
                                }
        with open(syncini_file, 'w') as configfile:
            configur.write(configfile)
        return

    configur.read(syncini_file)
    syncuser = configur.get('DEFAULT', 'SYNC_USER')
    syncon = configur.getboolean('DEFAULT', 'SYNC_ON')

    if (syncon):
        syncfacility = Facility.get_default_facility()

        if (syncfacility is not None):
            syncfacilityid = syncfacility.id
            syncpass = "sync" + syncfacilityid
            syncserver = configur.get('DEFAULT', 'SYNC_SERVER')
            syncdelay = configur.getfloat('DEFAULT', 'SYNC_DELAY')
            threading.Timer(syncdelay, run_sync).start()
            main(["manage", "sync", "--baseurl", syncserver, "--username", syncuser, "--password", syncpass, "--facility", syncfacilityid, "--verbosity", "3"])
run_sync()
