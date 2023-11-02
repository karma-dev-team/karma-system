from attrs import define


class Event:
    pass


event = define(kw_only=True, slots=True)