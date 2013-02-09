## Script (Python) "get_macros_wrapper"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##title=
##parameters=vdata

from ZODB.POSException import ConflictError

try:
    return context.get_macros(vdata)
except ConflictError:
    raise
except:
    return None
