# pylint: disable=W0401
from django.core.exceptions import ImproperlyConfigured
from django.db.backends.oracle.base import *
from django.db.backends.oracle.base import DatabaseWrapper as DjDatabaseWrapper

import cx_Oracle


class DatabaseWrapper(DjDatabaseWrapper):

    def __init__(self, *args, **kwargs):
        super(DatabaseWrapper, self).__init__(*args, **kwargs)
        if 'POOL' not in self.settings_dict: 
            poolconfig = { 'min': 1, 'max': 2, 'increment': 1 }
        else:
            poolconfig = self.settings_dict['POOL']
            if ('min' not in poolconfig or
                'max' not in poolconfig or
                'increment' not in poolconfig):
                raise ImproperlyConfigured('POOL database option requires \'min\', \'max\', and \'increment\'') 
            poolconfig['min'] = int(poolconfig['min'])
            poolconfig['max'] = int(poolconfig['max'])
            poolconfig['increment'] = int(poolconfig['increment'])

        self.pool = cx_Oracle.SessionPool(
            user=self.settings_dict['USER'],
            password=self.settings_dict['PASSWORD'],
            dsn=self.settings_dict['NAME'], **poolconfig)

    def get_new_connection(self, conn_params):
        conn_params.update({
            'pool': self.pool,
        })
        return super(DatabaseWrapper, self).get_new_connection(conn_params)

    def _close(self):
        if self.connection is not None:
            with self.wrap_database_errors:
                return self.pool.release(self.connection)
