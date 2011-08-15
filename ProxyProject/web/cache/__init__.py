
from os.path import dirname, join, abspath


relPath = lambda filename : abspath( join( dirname( __file__ ), filename  ) )

MAKO_C = relPath("mako/")


