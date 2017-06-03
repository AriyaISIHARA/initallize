"""__init__ sample without __all__ definition"""

from .inner_module import ClassSingle
from .inner_module import ClassSingleWithComment  # comment
from .inner_module import \
     ClassSingleBackSlashed
from outer_module import OuterClass
from outer_module import Class as OuterClassAlias

from .inner_module import (    # comment
    MultiLineClass1,  # a block comment may go here
    MultiLineClass2,
    Class as MultiLineClassAlias,
    INNER_MODULE_CONSTANT,
    inner_module_function  # without trailing comma
)

from outer_module import (
     outer_module_function,  # with trailing comma
)
