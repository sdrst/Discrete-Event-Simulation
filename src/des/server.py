"""Per-server state tracking for a single queueing stage."""


class Server:
    """Tracks busy/idle state and timing for one server in a queue."""

    def __init__(self):
        self.id = 0
        self.busy = False
        self.idle_time = 0.0
        self.start = 0.0
        self.end = 0.0

    def isBusy(self):
        return self.busy == True
