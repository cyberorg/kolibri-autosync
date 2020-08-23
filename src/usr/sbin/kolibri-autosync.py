#!/usr/bin/python3
# MSS Cloud sync for multifacilities on user device
import logging
import threading
import os
import sys

from kolibri.utils.cli import main

def facility_sync(syncserver, syncuser, syncpass, syncfacilityid):
    pid = os.fork()
    if pid == 0:
        main(["manage", "sync", "--baseurl", syncserver, "--username", syncuser, "--password", syncpass, "--facility", syncfacilityid, "--verbosity", "3"])
    else:
        os.waitpid(pid, 0)

def run_sync():
#    logging.basicConfig(level=logging.INFO)
#    logging.disable(logging.INFO)
#    logging.disable(logging.WARNING)
    from configparser import ConfigParser
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

    configur.read(syncini_file)
    syncon = configur.getboolean('DEFAULT', 'SYNC_ON')
    syncdelay = configur.getfloat('DEFAULT', 'SYNC_DELAY')
    if (syncon):
        threading.Timer(syncdelay, run_sync).start()
        from django.core.management import execute_from_command_line
        sys.__stdout__ = sys.stdout
        sys.stdout = open(os.devnull, 'w')
        execute_from_command_line(sys.argv)
        sys.stdout = sys.__stdout__
        from kolibri.core.auth.models import Facility
        syncfacilities = Facility.objects.filter()
        syncuser = configur.get('DEFAULT', 'SYNC_USER')
        syncserver = configur.get('DEFAULT', 'SYNC_SERVER')
        if syncfacilities:
            logging.info(syncfacilities)
            for syncfacility in syncfacilities:
                syncfacilityid = syncfacility.id
                syncpass = "sync" + syncfacilityid
                if syncfacilityid in configur:
                    syncuser = configur.get(syncfacilityid, 'SYNC_USER')
                    try:
                        syncpass = configur.get(syncfacilityid, 'SYNC_PASS')
                    except:
                        syncpass = "sync" + syncfacilityid
                    syncdelay = configur.getfloat(syncfacilityid, 'SYNC_DELAY')
                    syncserver = configur.get(syncfacilityid, 'SYNC_SERVER')
                else:
                    configur[syncfacilityid] = { }
                    with open(syncini_file, 'w') as configfile:
                        configur.write(configfile)
#                    configur.read(syncini_file)

                facility_sync(syncserver, syncuser, syncpass, syncfacilityid)
run_sync()
