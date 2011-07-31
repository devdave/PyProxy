"""
    Root of Web, intra-package/module access should funnel through here
"""
#plugins
from txweb import Site
#app
from root import Root



site = Site(Root())
