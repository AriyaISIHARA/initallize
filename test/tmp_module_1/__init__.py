"""__init__ sample without __all__ definition"""

from .inner_module import (
    InnerModuleClass,
    INNER_MODULE_CONSTANT,
    inner_module_function,
)


'''
some other stuffs may go before __all__ definition,
such as this comment.
'''


__all__ = (
    'an out-dated __all__ definition may go here,',
    'which can be multi-lined.'
)

# some other stuffs may go after __all__ definition,
# such as this comment.
#
# CAUTION:
#     The current version of initallize
#     REMOVES anything after __all__ definition.
