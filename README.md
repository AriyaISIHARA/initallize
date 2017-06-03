# initallize
====

## Overview

The present tool *initallize* reads `__init__.py` files
in the specified directory tree, to
create or update the definition of the `__all__` attribute
in each `__init__.py` file.

## Caution

Using the present tools from a shell may cause a destructive result;
he removes everything after the first match
`/^__all__\s+=/`, including the match.

Detecting imported identifiers is proceeded by
adhoc regex implementation,
which coveres only *usual* `__init__.py` appearance.
Any output is absolutely not warranted if
it covers all the identifiers.

## Demo

For example, the following file

```test/input_readme_demo_py.src
from .beef import BeefHam as Ham
from .eggs import (
    AbstractEgg as Egg,
    ChickenEgg,
    ElephantEgg,  # extentional egg
)
from mails import spam
from prices import (
    PRICE_BEEF_HAM as PRICE_HAM,
    PRICE_CHICKEN_EGG,
    PRICE_ELEPHANT_EGG  # the last colon may be omitted 
)
```

will be overwritten as follows:

```test/output_readme_demo_py.src
from .beef import BeefHam as Ham
from .eggs import (
    AbstractEgg as Egg,
    ChickenEgg,
    ElephantEgg,  # extentional egg
)
from mails import spam
from prices import (
    PRICE_BEEF_HAM as PRICE_HAM,
    PRICE_CHICKEN_EGG,
    PRICE_ELEPHANT_EGG  # the last colon may be omitted 
)


__all__ = (
    'spam',
    'ChickenEgg',
    'Egg',
    'ElephantEgg',
    'Ham',
    'PRICE_CHICKEN_EGG',
    'PRICE_ELEPHANT_EGG',
    'PRICE_HAM',
)
```

## Technical Overview

Constructor `initallize.Initallize(dname)`
takes one positional argument `dname` to specify
the directory of one `__init__.py` file,
and it seeks the code to fetch identifier names.

- First, it searches `/^__all__\s+=/` occurrence and
  read the code before the match; it reads the whole code
  if no `__all__` definition is found.
- Next, it seeks
  `(from <something>)? import (<something> as)? <identifier>`
  to update the identifiers list.
- Last, it seeks
  `from <something> import (<multiline>)`
  to recognize multi-lined importation.
  For each match, from the body `<multiline>`, it seeks
  `(<something> as)? <identifier>`
  to update the identifiers list.
  
The above process is done at the constructor call,
and the instance holds the 'before_all' code of the
original `__init__.py` and the detected identifier names.

Calling `write(file)` method writes down the
'all_updated' `__init__.py` file to `file`.

## Requirement

python 3.6

or later; the author loves PEP498.

## Usage

### Command-line Usage

From a shell,

```
python 'initall' <root dir>
```

will change every `__init__.py` under the `<root dir>` directory.

### Class Reference

- class *initallize.Initallize*(dname)
    Reads `<dname>/__init__.py` and searches identifiers.

  - *write*(file)
    Writes updated `__init__.py` to `file`.

## Install

The package consists of a single file `src/initallize.py`;
download the file, or copy source.

## Contribution

The present tool is produced basically for my own use,
and thus already suffices.
So, the author does not intend to upgrade the tool any more.
Nevertheless, the present tool leaves many features
to be improved:

- Much more stable analyzing of `__init__.py`
- Support variant indentation
- Support variant style of sorting identifiers
  (currently lower_case, CamelCase, UPPER_CASE, alphabetical order)
- Support `# noqa: F401` style

PR satisfying the above or other issues,
or testcases criticizing the issues are very welcome.
(For testcases, please `@skip` new testcases so that
the PR can be directly merged)

## Poems

### Versus noqa

Speaking of `# noqa: F401` style,
I was intending to make the tool that
alignes `# noqa: F401` occurrence,
at the very beginning of this project:

```
from .ham import Ham  # noqa: F401
from .egg import Egg
from .spam import Spam  # noqa: F401
```

to

```
from .ham import Ham    # noqa: F401
from .egg import Egg    # noqa: F401
from .spam import Spam  # noqa: F401
```

I had googled such tools, but not found any so far.
However, as a byproduct, my mentor Stack Overflow
told me that `__all__` definition can restrain
my fussy uncle Flake8 from saying F401
without pittyful block comments.
Though I admit that it is also pittyful or contrary to DRY to
enumerate *every* identifiers appearing in `__init__.py`,
I chose `__all__` from `noqa` and `__all__`
(please tell me another better one, if exists).

Making an excuse, in other parts of my source code,
`__all__` will very unlikely appear;
I won't do `from egg import *` because I don't eat egg shell.
On the other hand, `# noqa: F401`
can often visit my code during development,
and they are expected to leave the code eventually.
Consequently, I do sometimes `% grep -r noqa .` or something like that,
but never for `__all__`.

Thus, I *presently* do my init file with `__all__`,
but not *pleasantly*.
I still miss my not-implemented tool 'noqalign'.

### Against string literal

In order to avoid string literals,
I thought of supporting the following crazy style:

```
from .ham import Ham
from .egg import Egg
from .spam import Spam

__all__ = tuple(o.__name__ for o in (
    Ham,
    Egg,
    Spam,
))
```

which is fail-fast on misspelling.
The problem was that
base-typed constant objects do not have attribute `__name__`.

### Conclusion

I will appriciate someone who
tell me a DRY, no noqa style of `__init__.py`.

## Author

[AriyaISIHARA](https://github.com/AriyaISIHARA)
