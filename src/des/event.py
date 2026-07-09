"""Scheduled event representation used by the simulation's event heap."""

from .server import Server


class Event:
    """A single scheduled event: an arrival, a primary service, or a secondary service."""

    def __init__(self):
        self.arrive = 0.0
        self.primary = 0.0
        self.secondary = 0.0
        self.event_time = 0.0
        self.event_type = 0
        self.queue_t = 0.0
        self.server = Server()
