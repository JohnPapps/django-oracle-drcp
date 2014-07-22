# pylint: disable=W0401
from django.db.backends.oracle.base import *
from django.db.backends.oracle.base import DatabaseWrapper as DjDatabaseWrapper

import cx_Oracle


class DatabaseWrapper(DjDatabaseWrapper):

    def __init__(self, *args, **kwargs):
        super(DatabaseWrapper, self).__init__(*args, **kwargs)
        self.pool = cx_Oracle.SessionPool(
            user=self.settings_dict['USER'],
            password=self.settings_dict['PASSWORD'],
            dsn=self.settings_dict['NAME'], **self.settings_dict['POOL'])

    def get_new_connection(self, conn_params):
        conn_params.update({
            'pool': self.pool,
        })
        return super(DatabaseWrapper, self).get_new_connection(conn_params)

    def _close(self):
        if self.connection is not None:
            with self.wrap_database_errors:
                return self.pool.release(self.connection)
