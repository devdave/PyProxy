
from ProxyProject.web.controllers.base import * 
from ProxyProject.web.static import relPath

from twisted.web.static import File

import traceback
from StringIO import StringIO
import sys


class Console(Base):
    

    index = File(relPath("console/index.html"))
    
    @expose    
    def process(self, request, **kwargs):
        code = kwargs.get('code', None)
        if code is None:
            code = request.args['code'][0]
        
        try:
            compiled = compile(code, "<string>", "exec")
        except Exception as e:
            request.write("<pre>")
            request.write("Compilation error: %s" % e)
            request.write(traceback.format_exc())
            request.write("</pre>")

            request.finish()
            return NOT_DONE_YET
            
        buffer = StringIO()
        
        
        
        #Eventually for out of band/line information
        outofband = dict()
        scope = dict(controller=self, store = request.site.store, oob = outofband)
        
        try:
            oldStdout = sys.stdout
            oldStderr = sys.stderr
            sys.stdout = buffer
            sys.stderr = buffer
            exec compiled in scope
        except Exception as e:
            request.write("<pre>")
            request.write("Exec error: %s:%s" % (type(e), e))
            request.write(traceback.format_exc())
            request.write("</pre>")
        else:
            buffer.seek(0)
            request.write(buffer.read())
        finally:
            sys.stdout = oldStdout
            sys.stderr = oldStderr
            
        request.finish()
        return NOT_DONE_YET
        
            
            
        
        
    
    