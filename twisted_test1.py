
from twisted.internet import reactor
from twisted.python import log
import sys
log.startLogging(sys.stdout)

from myproxy import ProxyFactory
from myweb import GetSite
from os.path import (dirname, abspath, join)
from config import Config
Config['web']["root"] = join(abspath(dirname(__file__)) , Config['web']["root"] )



reactor.listenTCP(Config['web']['port'], GetSite(Config))
reactor.listenTCP(Config['proxy']['port'], ProxyFactory())
reactor.run()