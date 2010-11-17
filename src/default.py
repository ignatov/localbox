""" Localbox program. """

import e32
import sys
import os
import socket
from appuifw import *

def bootstrap():
    """ Adds to sys.path necessary paths. """
    for path in ('c:\\data\\python\\lib', 'e:\\python\\lib'):
        if os.path.exists(path):
            sys.path.append(path)

def select_default_access_point():
    """ Select the default access point. Return True if the selection was done or False if not. """
    aps = socket.access_points()
    if not aps:
        note(u"No access points available", "error")
        return False

    ap_labels = [x['name'] for x in aps]
    item = popup_menu(ap_labels, u"Access points:")
    if item is None:
        return False

    socket.set_default_access_point(aps[item]["name"])

    return True

def main():
    """ Main routine. """
    bootstrap()

    from localbox.synchronizer import Synchronizer

    if select_default_access_point():
        note(u"sync started", "info")
        e32.Ao_timer().after(1)
        Synchronizer("E:\\testing.ini").sync()
        note(u"sync finished", "info")

if __name__ == "__main__":
    sys.exit(main())
