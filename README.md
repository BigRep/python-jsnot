# python-jsnot
A smarter JSON/value wrapper providing a number of convenient methods for
faster access and manipulation of properties.

`JSNOT` can be considered as a simple value wrapper with a number of convenient
methods. Some of these methods (i.e. `at_path`, `get`, `has`, and `__get__item`)
are only applicable if the wrapped value is a `dict` (e.g. JSON). These methods
accept a string denoting a backslash separated keys (a **path**), so the following:

```python
my_dict = {...}
my_dict['some']['keys']['to']['my']['value']
```
becomes:

```python
my_jsnot = JSNOT(my_dict)
my_jsnot['some\\keys\\to\\my\\value']
```

All available methods:

 * `at_path(path)`: a `JSNOT` object wrapping value at given path
 * `get(path, default)`: same as `as_path` but returns `default` if not available
 * `has(path)`: verifies if a value is available at given `path`
 * `satisfy(calssinfo)`: check if internal value is an instance of `classinfo`
 * `cast(typ)`: casts internal value to given type (`typ`)

## Quick start
Consider following JSON file:

```json
{
  "module": {
    "name": "JSNOT",
    "version": "0.1",
    "python2": false,
    "dependencies": ["re", "json"]
  },
  "maintainer": "Yan Foto"
}
```

This is how it works:

```python
from bigrep.jsnot import JSNOT

with open('myfile.json') as j:
  jsnot = JSNOT(j)

jsnot['module\\version']                       # '0.1' (str)
jsnot.at_path('module\\version').satisfy(int)  # False
jsnot.at_path('module\\version').cast(float)   # 0.1 (int)
jsnot['module\\dependencies'][0]               # re
jsnot.has('module\\alias')                     # False
jsnot.get('module\\alias', 'JSN0T')            # 'JSN0T'
```
