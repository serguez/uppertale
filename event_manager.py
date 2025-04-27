from collections import defaultdict

class Event:
    def __init__(self, kind, payload=None):
        self.kind = kind          # ex. "LEVER_PULLED"
        self.payload = payload    # ex. {"id": "L42"}

class EventManager:
    def __init__(self):
        self._subs = defaultdict(list)

    def subscribe(self, kind, callback):
        self._subs[kind].append(callback)

    def post(self, event: Event):
        for cb in self._subs[event.kind]:
            cb(event)