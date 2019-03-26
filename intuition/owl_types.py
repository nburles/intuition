import enum

class OWLTypes(enum.Enum):
    SOLAR = 'solar'
    ELECTRICITY = 'electricity'
    WEATHER = 'weather'

class ChannelTypes(enum.Enum):
    GENERATED = 'generated'
    EXPORTED = 'exported'
    USED = 'used'

class ControlTypes(enum.Enum):
    START = 'start'
    END = 'end'

