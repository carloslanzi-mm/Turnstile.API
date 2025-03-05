import copy

from flambda_app import helper
from flambda_app.database.mysql import MySQLConnector
from flambda_app.database.redis import RedisConnector
from flambda_app.enums.messages import MessagesEnum
from flambda_app.exceptions import DatabaseException, ValidationException, ServiceException
from flambda_app.filter_helper import filter_xss_injection
from flambda_app.helper import get_function_name
from flambda_app.logging import get_logger
from flambda_app.repositories.v1.mysql.turnstile_repository import TurnstileRepository
from flambda_app.vos.turnstile import TurnstileVO


class TurnstileService:
    DEBUG = False
    REDIS_ENABLED = False

    def __init__(self, logger=None, mysql_connector=None, redis_connector=None,
                 turnstile_repository=None):
        self.logger = logger if logger is not None else get_logger()
        self.mysql_connector = mysql_connector if mysql_connector is not None else MySQLConnector()
        self.turnstile_repository = turnstile_repository if turnstile_repository is not None \
            else TurnstileRepository(mysql_connection=self.mysql_connector.get_connection())

        self.exception = None
        self.debug(self.DEBUG)

    def debug(self, flag: bool = False):
        self.DEBUG = flag
        self.turnstile_repository.debug = self.DEBUG

    def list(self, request: dict):
        self.logger.info(f'method: {get_function_name()} - request: {request}')

        data = []
        where = request['where']

        # exclude deleted
        where['deleted_at'] = None

        try:
            # data = self.turnstile_repository.list(
            #     where=where, offset=request['offset'], limit=request['limit'],
            #     order_by=request['order_by'], sort_by=request['sort_by'], fields=request['fields']
            # )
            # if data:
            #     data = [TurnstileVO(item, default_values=False).to_api_response() for item in data]
            # if self.turnstile_repository.get_exception():
            #     raise DatabaseException(MessagesEnum.LIST_ERROR)

            offset = request['offset']
            limit = request['limit']
            order_by = request['order_by']
            sort_by = request['sort_by']
            fields = request['fields']
            data = self.turnstile_repository.list(
                where=where, offset=offset, limit=limit, order_by=order_by,
                sort_by=sort_by, fields=fields)

            # convert to vo and prepare for api response
            if data:
                vo_data = []
                for item in data:
                    vo_data.append(TurnstileVO(item, default_values=False).to_api_response())
                data = vo_data

            # set exception if it happens
            if self.turnstile_repository.get_exception():
                raise DatabaseException(MessagesEnum.LIST_ERROR)

        except Exception as err:
            self.logger.error(err)
            self.exception = err

        return data

    def count(self, request: dict):
        self.logger.info('method: {} - request: {}'
                         .format(get_function_name(), request))

        total = 0
        where = request['where']
        if where == dict():
            where = {
                'active': 1
            }

        # exclude deleted
        where['deleted_at'] = None

        try:
            order_by = request['order_by']
            sort_by = request['sort_by']
            total = self.turnstile_repository.count(
                where=where, order_by=order_by, sort_by=sort_by)
        except Exception as err:
            self.logger.error(err)
            self.exception = DatabaseException(MessagesEnum.LIST_ERROR)

        return total

    def find(self, request: dict):
        self.logger.info('method: {} - request: {}'.format(get_function_name(), request))
        raise ServiceException(MessagesEnum.METHOD_NOT_IMPLEMENTED_ERROR)

    def get(self, request: dict, id):
        self.logger.info(f'method: {get_function_name()} - request: {request}, id: {id}')

        data = []
        where = request.get('where', {})

        try:
            data = self.turnstile_repository.get(
                id, key=self.turnstile_repository.UUID_KEY, where=where, fields=request['fields'])
            if data:
                data = TurnstileVO(data, default_values=False).to_api_response()
            if self.turnstile_repository.get_exception():
                raise DatabaseException(MessagesEnum.FIND_ERROR)
        except Exception as err:
            self.logger.error(err)
            self.exception = err
        return data

    def create(self, request: dict):
        self.logger.info(f'method: {get_function_name()} - request: {request}')

        data = request.get('where', {})
        if not data:
            raise ValidationException(MessagesEnum.REQUEST_ERROR)

        try:
            turnstile_vo = TurnstileVO(data)
            created = self.turnstile_repository.create(turnstile_vo)
            if created:
                return turnstile_vo.to_api_response()
            raise DatabaseException(MessagesEnum.CREATE_ERROR)
        except Exception as err:
            self.logger.error(err)
            self.exception = err
        return None

    def update(self, request: dict, uuid):
        self.logger.info(f'method: {get_function_name()} - request: {request}')

        original_turnstile = self.turnstile_repository.get(
            uuid, key=self.turnstile_repository.UUID_KEY)
        if original_turnstile is None:
            raise DatabaseException(MessagesEnum.FIND_ERROR)

        data = request['where']
        if self.DEBUG:
            self.logger.info('method: {} - data: {}'.format(get_function_name(), data))

        # validate the request payload
        self.validate_data(data, original_turnstile)

        # update original employee with update data
        original_turnstile.update(data)
        data = original_turnstile

        try:
            if data == dict():
                raise ValidationException(MessagesEnum.REQUEST_ERROR)

            data.update({'updated_at': helper.datetime_now_with_timezone()})
            turnstile_vo = data

            updated = self.turnstile_repository.update(data, uuid,
                                                       key=self.turnstile_repository.UUID_KEY)

            if updated:
                # convert to vo and prepare for api response
                data = turnstile_vo.to_api_response()
            else:
                data = None
                # set exception if it happens
                raise DatabaseException(MessagesEnum.UPDATE_ERROR)

        except Exception as err:
            self.logger.error(err)
            self.exception = err

        return data

    def delete(self, request: dict, uuid):
        self.logger.info(f'method: {get_function_name()} - request: {request}')

        original_turnstile = self.turnstile_repository.get(
            uuid, key=self.turnstile_repository.UUID_KEY)
        if original_turnstile is None:
            raise DatabaseException(MessagesEnum.FIND_ERROR)

        try:
            if self.turnstile_repository.soft_delete(value=uuid,
                                                     key=self.turnstile_repository.UUID_KEY):
                return True
            raise DatabaseException(MessagesEnum.SOFT_DELETE_ERROR)
        except Exception as err:
            self.logger.error(err)
            self.exception = err
        return False

    def validate_data(self, data, original_turnstile):
        allowed_fields = list(original_turnstile.to_dict().keys())
        try:
            for field in ['uuid', 'id', 'updated_at', 'created_at', 'deleted_at']:
                allowed_fields.remove(field)
        except Exception as err:
            self.logger.error(err)
        for field in data.keys():
            if field not in allowed_fields:
                exception = ValidationException(MessagesEnum.VALIDATION_ERROR)
                exception.params = [filter_xss_injection(data[field]), filter_xss_injection(field)]
                exception.set_message_params()
                raise exception
