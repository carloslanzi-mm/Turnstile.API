from flambda_app.config import get_config
from flambda_app.logging import get_logger
from flambda_app.services.v1.turnstile_service import TurnstileService


class TurnstileManager:
    def __init__(self, logger=None, config=None, turnstile_service=None):
        self.logger = logger if logger is not None else get_logger()
        # configurations
        self.config = config if config is not None else get_config()
        # service
        self.turnstile_service = turnstile_service if turnstile_service is not None \
            else TurnstileService(self.logger)

        # exception
        self.exception = None

        # debug
        self.DEBUG = None

    def debug(self, flag: bool = False):
        self.DEBUG = flag
        self.turnstile_service.debug(self.DEBUG)

    def list(self, request: dict):
        data = self.turnstile_service.list(request)
        if (data is None or len(data) == 0) and self.turnstile_service.exception:
            self.exception = self.turnstile_service.exception
            raise self.exception
        return data

    def count(self, request: dict):
        total = self.turnstile_service.count(request)
        if self.turnstile_service.exception:
            self.exception = self.turnstile_service.exception
            raise self.exception
        return total

    def get(self, request: dict, id):
        data = self.turnstile_service.get(request, id)
        if (data is None) and self.turnstile_service.exception:
            self.exception = self.turnstile_service.exception
            raise self.exception
        return data

    def create(self, request: dict):
        data = self.turnstile_service.create(request)
        if (data is None) and self.turnstile_service.exception:
            self.exception = self.turnstile_service.exception
            raise self.exception
        return data

    def update(self, request: dict, uuid):
        data = self.turnstile_service.update(request, uuid)
        if (data is None) and self.turnstile_service.exception:
            self.exception = self.turnstile_service.exception
            raise self.exception
        return data

    def delete(self, request: dict, uuid):
        result = self.turnstile_service.delete(request, uuid)
        if (result is None) and self.turnstile_service.exception:
            self.exception = self.turnstile_service.exception
            raise self.exception
        return result
