#!/usr/bin/env python

import sys, os

print "Starting up..."

os.environ["KURADIR"]="/usr/local/share/kura"

try:
    from kuraclient import main
except:
    sys.path.append("/usr/local/share/kura")
    from kuraclient import main
main.main()
