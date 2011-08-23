
from twisted.internet.task import LoopingCall

from store import Store
import bus


def initialize(user_config = None):
    config = dict(storePath = "./store.data", save_interval = 10 )
    if user_config:
        config.update(user_config)
    try:
        store = Store.readFrom(config['storePath'])
    except Exception as e:
        print "Failed restoring old data store `%s`, creating pristine store" %e
        store = Store()
    
    storeSaver = lambda : Store.saveTo(store, config['storePath'])
    storeLoop = LoopingCall(storeSaver)
    storeLoop.start(config['save_interval'], now=False)
    
    bus.register("data.store.addRecord", store.addRecord )
    #Hack to ensure Store instance is accessible elsewhere
    bus.register("data.store", lambda : store )
    
    