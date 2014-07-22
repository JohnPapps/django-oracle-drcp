django-oracle-drcp
==================
A Django database backend for Oracle with DRCP.

Developed against Oracle 11.2 with cx_Oracle 5.1.2 in Django 1.6 with Python 3.3

Please e-mail thoughts, comments, and suggestions to me, s@johnpapps.com

Configuration
-------------
Ensure you have a tnsnames.ora entry augmented with SERVER=POOLED.
Modify your database entry to reference the django-oracle-drcp backend.
Set 'NAME' to the name of the appropriate tns entry.

Configure DRCP options.
Add an 'OPTIONS' entry to your database dict, and set it to
a dict as follows:
```
'OPTIONS': {
    'purity': cx_Oracle.ATTR_PURITY_NEW,
    'cclass': 'YourConnectionClass',
}
```

'purity' may be set to cx_Oracle.ATTR_PURITY_NEW (which means the session must
be new without any priort session state) or cx_Oracle.ATTR_PURITY_SELF
(meaning the session may have been used before).
You may also set 'purity' to cx_Oracle.ATTR_PURITY_DEFAULT for the default
behaviour defined by Oracle.

'cclass' is set to the string used to define the connection class for DRCP.
You will see entries for each class in queries for stats such as
"select * from v$cpool_cc_stats"

Next, add a 'POOL' entry to your database dict, and set it to a dict as
follows:
```
'POOL': {
    'min': 1,
    'max': 2,
    'increment': 1,
}
```

'min' is set to the minimum number of sessions that will be controlled by the
session pool.
'max' is set to the maximum number of sessions that the session pool can
control.
'increment' is set to the number of sessions that will be established when
additional sessions need to be created.

You may also include a 'timeout' option in the 'POOL' dict, set to the time
(in seconds) after which idle sessions will be terminated in order to maintain
an optimal number of open sessions.

Example
-------

```python
# settings.py
import cx_Oracle

databases = {
    'default': {
        'ENGINE': 'django-oracle-drcp',
        'NAME': 'my_drcp_db',
        'USER': 'my_db_user',
        'PASSWORD': 'my_password',
        'HOST': '',
        'PORT': '',
        'OPTIONS': {
            'purity': cx_Oracle.ATTR_PURITY_NEW,
            'cclass': 'myappname',
        },
        'POOL': {
            'min': 1,
            'max': 4,
            'increment': 2,
        }
    }
}
```
