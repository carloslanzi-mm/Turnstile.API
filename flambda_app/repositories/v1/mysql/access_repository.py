from datetime import datetime

from flambda_app.request_control import Order, Pagination, PaginationType
from flambda_app.repositories.v1.mysql import AbstractRepository
from flambda_app.vos.access import AccessV0


class AccessRepository(AbstractRepository):
    BASE_TABLE = 'access'
    BASE_SCHEMA = 'store'
    BASE_TABLE_ALIAS = 'a'
    PK = 'id'
    UUID_KEY = 'uuid'
    TURNSTILE_UUID = 'turnstile_uuid'

    def __init__(self, logger=None, mysql_connection=None):
        super().__init__(logger, mysql_connection)

    def create(self, access: AccessV0):
        keys = list(access.to_dict().keys())
        keys.remove(self.PK)
        keys_str = ",".join(keys)
        values_count = len(access.to_dict().values()) - 1
        values_str = ",".join(['%s' for _ in range(values_count)])

        sql = "INSERT INTO {} ({}) VALUES ({})".format(self.BASE_TABLE, keys_str, values_str)

        access_dict = access.to_dict()
        del access_dict[self.PK]
        values = tuple(access_dict.values())

        try:
            created = self._execute(sql, values)
            access.id = self.connection.insert_id()
            self.connection.commit()
            return True
        except Exception as err:
            self.logger.error(err)
            self.connection.rollback()
            self._exception = err
            created = False
        finally:
            self._close()
        return created

    # def update(self, access: AccessV0, value, key=None):
    #     key_type = '%s'
    #     if key is None:
    #         key = self.PK
    #
    #     keys = list(access.to_dict().keys())
    #     keys.remove(self.PK)
    #     keys.remove(self.UUID_KEY)
    #
    #     values = []
    #     update_data = []
    #     for k, v in access.to_dict().items():
    #         if k in keys:
    #             update_data.append('{}.{}=%s'.format(self.BASE_TABLE_ALIAS, k))
    #             values.append(v)
    #
    #     update_str = ",".join(update_data)
    #     sql = "UPDATE {} as {} SET {} WHERE {}.{} = {}".format(self.BASE_TABLE,
    #                                                            self.BASE_TABLE_ALIAS, update_str,
    #                                                            self.BASE_TABLE_ALIAS, key, key_type)
    #
    #     access_dict = access.to_dict()
    #     del access_dict[self.PK]
    #     del access_dict[self.UUID_KEY]
    #     values.append(value)
    #
    #     try:
    #         updated = self._execute(sql, values)
    #         if updated:
    #             self.connection.commit()
    #             return True
    #     except Exception as err:
    #         self.logger.error(err)
    #         self.connection.rollback()
    #         self._exception = err
    #         updated = False
    #     finally:
    #         self._close()
    #     return updated

    def get(self, value, key=None, where: dict = None, fields: list = None):
        key_type = '%s'
        if key is None:
            key = self.PK

        if where is None:
            where = dict()

        fields = '*' if not fields else ",".join([self.BASE_TABLE_ALIAS + '.' + v for v in fields])

        sql = "SELECT {} FROM {} as {} WHERE {} = {}".format(
            fields, self.BASE_TABLE, self.BASE_TABLE_ALIAS, key, key_type)

        if where:
            sql += " WHERE {}".format(self.build_where(where))

        try:
            result = self._execute(sql, value)
            item = result.fetchone()
            return AccessV0(item) if item else None
        except Exception as err:
            self.logger.error(err)
        finally:
            self._close()
        return None

    def list(self, where: dict, offset=None, limit=None, fields: list = None, sort_by=None,
             order_by=None):
        fields = '*' if not fields else ",".join([self.BASE_TABLE_ALIAS + '.' + v for v in fields])
        order_by = order_by or Order.ASC
        sort_by = sort_by or self.PK
        sort_by = ",".join([self.BASE_TABLE_ALIAS + '.' + v for v in sort_by]) if isinstance(
            sort_by, list) else self.BASE_TABLE_ALIAS + '.' + sort_by

        sql = "SELECT {} FROM {} as {}".format(fields, self.BASE_TABLE, self.BASE_TABLE_ALIAS)
        if where:
            sql += " WHERE {}".format(self.build_where(where))
        sql += " ORDER BY {} {} LIMIT {},{}".format(sort_by, order_by,
                                                    Pagination.validate(PaginationType.OFFSET,
                                                                        offset),
                                                    Pagination.validate(PaginationType.LIMIT,
                                                                        limit))

        try:
            result = self._execute(sql)
            return result.fetchall()
        except Exception as err:
            self.logger.error(err)
            self._exception = err

    def build_where(self, where):
        where_list = []
        for k, v in where.items():
            if v is None:
                where_value = '{} IS NULL'.format(self.BASE_TABLE_ALIAS + "." + k)
            else:
                where_value = '{} = {}'.format(self.BASE_TABLE_ALIAS + "." + k,
                                               '"{}"'.format(v) if isinstance(v, str) else v)
            where_list.append(where_value)
        where_str = " AND ".join(where_list)
        return where_str

    def count(self, where: dict, sort_by=None, order_by=None):
        if order_by is None:
            order_by = Order.ASC

        if sort_by is None:
            sort_by = self.PK
        elif isinstance(sort_by, list):
            sort_by_arr = [self.BASE_TABLE_ALIAS + '.' + v for v in sort_by]
            sort_by = ",".join(sort_by_arr)
        else:
            sort_by = self.BASE_TABLE_ALIAS + '.' + sort_by

        sql = "SELECT COUNT(1) as total FROM {} as {}".format(self.BASE_TABLE,
                                                              self.BASE_TABLE_ALIAS)

        if where != dict():
            where_str = self.build_where(where)
            sql = sql + " WHERE {}".format(where_str)

        sql = sql + " ORDER BY {} {}".format(sort_by, order_by)

        try:
            result = self._execute(sql)
            result = result.fetchone()
            result = result['total']
        except Exception as err:
            self.logger.error(err)
            self._exception = err
            result = 0
        finally:
            self._close()

        return result

    # def soft_delete(self, value, key=None):
    #     key_type = '%s'
    #     if key is None:
    #         key = self.PK
    #
    #     sql = "UPDATE {}.{} SET deleted_at = %s WHERE {} = {}".format(
    #         self.BASE_SCHEMA, self.BASE_TABLE, key, key_type)
    #
    #     data = (datetime.today(), value,)
    #     try:
    #         result = self._execute(sql, data)
    #         self.connection.commit()
    #     except Exception as err:
    #         self.logger.error("SQL: {} ".format(sql))
    #         self.logger.error("Params: {} ".format(data))
    #         self.logger.error(err)
    #         result = None
    #         self.connection.rollback()
    #     finally:
    #         self._close()
    #
    #     return result
