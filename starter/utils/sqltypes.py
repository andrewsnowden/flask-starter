"""
An SQLAlchemy type that stores JSON
"""

import json
from sqlalchemy import types
from sqlalchemy.ext.mutable import Mutable


class MutableDict(Mutable, dict):
    """
    A dictionary that keeps track of when it has been modified
    """

    @classmethod
    def coerce(cls, key, value):
        "Convert plain dictionaries to MutableDict."

        if not isinstance(value, MutableDict):
            if isinstance(value, dict):
                return MutableDict(value)

            # this call will raise ValueError
            return Mutable.coerce(key, value)
        else:
            return value

    def __setitem__(self, key, value):
        "Detect dictionary set events and emit change events."

        dict.__setitem__(self, key, value)
        self.changed()

    def __delitem__(self, key):
        "Detect dictionary del events and emit change events."

        dict.__delitem__(self, key)
        self.changed()


class Json(types.TypeDecorator):
    """
    A JSON type that can be serialized to the database. This type is not
    mutable, you must set it for it to be changed in the database
    """
    impl = types.Unicode

    def process_bind_param(self, value, engine):
        if value is None:
            return None

        return unicode(json.dumps(value))

    def process_result_value(self, value, engine):
        if value:
            return json.loads(value)
        else:
            return None


class JsonDict(types.TypeDecorator):
    """
    A JSON type that uses a MutableDict to keep track of when things have
    changed. This means you can set a value in the dictionary and it will be
    saved in the database, while the non-mutable type you would have to set the
    entire dictionary. e.g.

    >>> user.meta["title"] = "Dr"
    would be saved using the mutable type, but not using the standard Json
    dictionary
    """
    impl = types.Unicode

    def process_bind_param(self, value, engine):
        if value is None:
            return None

        return unicode(json.dumps(value))

    def process_result_value(self, value, engine):
        if value:
            return MutableDict(json.loads(value))
        else:
            return None
