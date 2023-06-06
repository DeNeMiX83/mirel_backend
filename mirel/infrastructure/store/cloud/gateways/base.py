from mirel.infrastructure.store.cloud.protocols import Service


class Gateway:
    def __init__(self, service: Service):
        self._service = service
