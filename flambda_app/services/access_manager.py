from flambda_app.config import get_config
from flambda_app.logging import get_logger
from flambda_app.services.v1.access_service import AccessService


class AccessManager:
    def __init__(self, logger=None, config=None, access_service=None):
        self.logger = logger if logger is not None else get_logger()
        # configurations
        self.config = config if config is not None else get_config()
        # service
        self.access_service = access_service if access_service is not None \
            else AccessService(self.logger)

        # exception
        self.exception = None

        # debug
        self.DEBUG = None

    def debug(self, flag: bool = False):
        self.DEBUG = flag
        self.access_service.debug(self.DEBUG)

    def list(self, request: dict):
        data = self.access_service.list(request)
        if (data is None or len(data) == 0) and self.access_service.exception:
            self.exception = self.access_service.exception
            raise self.exception
        return data

    def count(self, request: dict):
        total = self.access_service.count(request)
        if self.access_service.exception:
            self.exception = self.access_service.exception
            raise self.exception
        return total

    def get(self, request: dict, id):
        data = self.access_service.get(request, id)
        if (data is None) and self.access_service.exception:
            self.exception = self.access_service.exception
            raise self.exception
        return data

    def create(self, request: dict):
        data = self.access_service.create(request)
        if (data is None) and self.access_service.exception:
            self.exception = self.access_service.exception
            raise self.exception
        return data

    # def update(self, request: dict, uuid):
    #     data = self.access_service.update(request, uuid)
    #     if (data is None) and self.access_service.exception:
    #         self.exception = self.access_service.exception
    #         raise self.exception
    #     return data
    #
    # def delete(self, request: dict, uuid):
    #     result = self.access_service.delete(request, uuid)
    #     if (result is None) and self.access_service.exception:
    #         self.exception = self.access_service.exception
    #         raise self.exception
    #     return result
