
from os.path import dirname, abspath, join


relPath = lambda filename : abspath(join(dirname(__file__), filename ))

CSS = relPath("css/")
JS  = relPath("js/")
ROOT = relPath("root/index.html")