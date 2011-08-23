"""
    Acts as glue between twisted MyPRoxyClient(ProxyClient) and data.store
"""

from ProxyProject import data
from ProxyProject.data.record import Record

def proxyClientInit(proxyClient):
    proxyClient.pxRecord = Record(proxyClient)
    
def proxyClientFinish(proxyClient):
    if hasattr(proxyClient, "pxRecord"):
        data.bus.call("data.store.addRecord", proxyClient.pxRecord)
    else:
        #todo see if I can use Python warnings w/twisted
        print "WARNING: Missing pxRecord on proxyInstance"

def initialize():
    """
        Binds the functions above to the ProxyClient init and finish hook points in the bus
    """
    data.bus.register("proxy-client.init", proxyClientInit )
    data.bus.register("proxy-client.handleResponseEnd", proxyClientFinish)
