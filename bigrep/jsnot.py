# -*- coding: utf-8 -*-
"""**Convenient module to ease the use of JSON objects.**"""

import json
import re
from functools import reduce
from io import IOBase

__author__ = "Yan Foto"
__credits__ = ["Yan Foto"]
__license__ = "GNU AFFERO GENERAL PUBLIC LICENSE"
__version__ = "0.0.1"
__email__ = "source@bigrep.com"
__date__ = "18.04.2016"


class JSNOT(object):
    """A smarter JSON wrapper providing a number of convenient methods for
    faster access and manipulation of properties.

    It is excepted to initialize it with a JSON string or a filelike object
    containing the JSON data. It can also be initialized with any arbitrary
    type (thus the name JSNOT: NOT JSON!) in which case only ``satisfy`` and
    ``cast`` methods are usable.
    """

    DELIMITER_PATTERN = '\\\\(?!\\\\["/bfnrtu])'
    """Regex pattern used as delimiter for key sepeartion.

    Note:
        In JSON keys are not allowed to contain backslashes if it is not followed
        by one of the following characters:

        * ``"`` : quotation mark
        * ``\\`` : backslash
        * ``/`` : forwardslash
        * ``b`` : backspace
        * ``f`` : formfeed
        * ``n`` : newline
        * ``r`` : carriage return
        * ``t`` : horizontal tab
        * ``u`` : 4 hexadecimal digits

    See:
        http://www.json.org/
    """

    def __init__(self, value):
        """Initializes JSNOT.

        Args:
            value (str|IOBase): string or filelike object containing JSON

        Examples:
            >>> j = JSNOT('{"test": {"goes": {"deep": "19"}, "or": 20}}')
            >>> print j['test\\goes\\deep'] # equals to j['test']['goes']['deep']
            "19"
            >>> print j.at_path('test\\goes\\deep').cast(float)
            19.0
        """
        if isinstance(value, str):
            self._value = json.loads(value)
        elif isinstance(value, IOBase):
            self._value = json.load(value)
        else:
            self._value = value

    def at_path(self, path):
        """Property accessor but with a JSNOT object returned.

        Args:
            path (str): backslash separated path to desired property

        Returns:
            str: value at given path wrapped in a JSNOT object

        Note:
            see also ``satisfy``, ``cast``, and ``__getitem__`` methods
        """
        return JSNOT(self[path])

    def get(self, path, default):
        """Retrieves value at given path or provided default value.

        Args:
            path (str): desired path
            default: default value if no value is avalable at path

        Returns:
            str: value at given path if any, otherwise provided default value
        """
        try:
            return self.at_path(path)
        except LookupError:
            return default

    def has(self, path):
        """Verifies if a value exists under given path.

        Args:
            key (str): backslash separated path to desired property

        Returns:
            True if property exists otherwise False
        """
        try:
            self[path]
        except LookupError:
            return False

        return True

    def satisfy(self, classinfo):
        """Verifies if current value is an instance of given class.

        Args:
            classinfo: desired class

        Returns:
            True if current value is an instance of given class

        Raises:
            TypeError: if contents with Request are not of type classinfo
        """

        if not isinstance(self._value, classinfo):
            raise TypeError(classinfo)

        return self

    def cast(self, typ):
        """Casts contents of current Request to desired type.

        Args:
            typ: desired type to cast to

        Returns:
            casted value to desired type
        """

        val = self._value

        try:
            return type(val) if typ is not None else val
        except ValueError:
            raise ValueError(type)

    def __getitem__(self, item):
        """Item accessor on steroids: it also accepts backslash separated keys.

        Note:
            In JSON spec it is not allowed for key strings to contains backslashes.
            This fact is being used to have slashes as delimiters.

        Example:
            >>> j = JSNOT('{"test": {"goes": {"deep": true}, "or": false}}')
            >>> print j['test\\goes\\deep']
            True

        Args:
            item (str): backslash separated keys

        Returns:
            value of property given at backslash separated path.
        """
        root = self._value
        if isinstance(root, dict):
            parts = re.split(JSNOT.DELIMITER_PATTERN, item)

            root = reduce(lambda prev, cur: prev[cur], parts, root)

        return root

    def __repr__(self):
        return self._value.__repr__()

    def __str__(self):
        return self.__repr__()
