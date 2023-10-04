from collections import OrderedDict
from json import JSONEncoder, dumps


class Object:
    all = {}

    @staticmethod
    def read(q: dict, *args):
        if q is None:
            return None
        if isinstance(q, Object):
            return q
        if not isinstance(q, dict):
            return q
        for key, value in q.items():
            if isinstance(value, dict) and value.get("@type", False):
                q[key] = Object.all[value["@type"]].read(value)
        return Object.all[q["@type"]].read(q, *args)

    def __str__(self) -> str:
        return dumps(self, cls=Encoder, indent=4)

    def __bytes__(self):
        return dumps(self, cls=Encoder).encode('utf-8')

    def __bool__(self) -> bool:
        return True

    def __eq__(self, other) -> bool:
        return self.__dict__ == other.__dict__

    def __len__(self) -> int:
        return len(self.__str__())

    def __call__(self):
        pass

    def __getitem__(self, item):
        return getattr(self, item)


class Encoder(JSONEncoder):
    def default(self, o: Object):
        content = o.__dict__
        o = getattr(o, "ID", "")
        r = OrderedDict([("@type", o)] + [i for i in content.items()])
        if r.get("extra"):
            r["@extra"] = r.pop("extra")
        return r

class Location(Object):
    """
    Describes a location on planet Earth

    Attributes:
        ID (:obj:`str`): ``Location``

    Args:
        latitude (:obj:`float`):
            Latitude of the location in degrees; as defined by the sender
        longitude (:obj:`float`):
            Longitude of the location, in degrees; as defined by the sender

    Returns:
        Location

    Raises:
        :class:`telegram.Error`
    """
    ID = "location"

    def __init__(self, latitude, longitude, **kwargs):

        self.latitude = latitude  # float
        self.longitude = longitude  # float

    @staticmethod
    def read(q: dict, *args) -> "Location":
        latitude = q.get('latitude')
        longitude = q.get('longitude')
        return Location(latitude, longitude)

class SearchChatsNearby(Object):
    """
    Returns a list of users and location-based supergroups nearby. The list of users nearby will be updated for 60 seconds after the request by the updates updateUsersNearby. The request should be sent again every 25 seconds with adjusted location to not miss new chats

    Attributes:
        ID (:obj:`str`): ``SearchChatsNearby``

    Args:
        location (:class:`telegram.api.types.location`):
            Current user location

    Returns:
        ChatsNearby

    Raises:
        :class:`telegram.Error`
    """
    ID = "searchChatsNearby"

    def __init__(self, location, extra=None, **kwargs):
        self.extra = extra
        self.location = location  # Location

    @staticmethod
    def read(q: dict, *args) -> "SearchChatsNearby":
        location = Object.read(q.get('location'))
        return SearchChatsNearby(location)

class GetSuperGroupMembers(Object):
    ID = "getSupergroupMembers"

    def __init__(self, supergroup_id, flt=None, offset=0, limit=200, extra=None, **kwargs):
        self.extra = extra
        self.supergroup_id = supergroup_id
        self.offset = offset
        self.filter = flt
        self.limit = limit

    @staticmethod
    def read(q: dict, *args) -> "GetSuperGroupMembers":
        _id = Object.read(q.get('supergroup_id'))
        _offset = Object.read(q.get('offset'))
        _limit = Object.read(q.get('limit'))
        _filter = Object.read(q.get('filter'))
        return GetSuperGroupMembers(_id, _filter, _offset, _limit)
