from twisted.python.rebuild import rebuild
from twisted.internet import reactor
from os.path import exists, isdir, dirname
from os import stat
from stat import ST_MTIME
import sys

class ModuleReloader(object):

    @classmethod
    def WatchThis(cls, path):
        if not isdir(path):
            path = dirname(path)
        list = []
        for name, module in sys.modules.items():
            if getattr(module, "__file__", "").startswith(path):
                list.append(module)
                
        return cls(list)
    
    def __init__(self, watchlist = [] ):
        self.watchlist = {}
        for module in watchlist:
            fileName = module.__file__
            if fileName.endswith(".pyc"):
                fileName = fileName[:-1]
            assert exists(fileName)
            self.watchlist[module] = (fileName ,  stat(fileName)[ST_MTIME])
        reactor.callLater(10, self)

        
    def __call__(self):
        try:
            for module, (file, ts) in self.watchlist.items():
                newTS = stat(file)[ST_MTIME]
                if ts != newTS:
                    self.watchlist[module] = (file ,  newTS)
                    rebuild(module)
                    print "Reloaded %s " % module
        finally:        
            reactor.callLater(10, self)
