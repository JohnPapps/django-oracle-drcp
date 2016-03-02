# Notes on Performance

## Alternatives

Django supports persistent connections per process as described in the
[Databases](https://docs.djangoproject.com/en/1.9/ref/databases/)
documentation. This may use a lot of memory depending on the application
configuration, e.g. how many servers are in useand how many processes are
permitted per server. However, this provides maximum performance while memory
lasts.

## How does DRCP work?

Oracle Database Resident Connection Pooling (DRCP) allows all of these
processes to share a limited number of pre-allocated connections allocated by
the database server. It is important however to understand that if more
connections are attempted than are supported by the pool, then some connections
will have to wait. However, if a process started by a WSGI application server
is idle, it may not need a connection. There is still a performance advantage
in having that process already started and ready to receive requests.

For more information, take a look at these links:

 * [Blog post on cx_Oracle and DRCP](https://blogs.oracle.com/opal/entry/python_cx_oracle_and_oracle)
 * [Whitepaper on DRCP](http://www.oracle.com/technetwork/topics/php/php-scalability-ha-twp-128842.pdf)

## How fast is DRCP vs Persistent Connections?

The test environment producing the results below is as Follows:

 * CentOS 6
 * Python 3.4.2 (rh-python34 from CentOS Software Collections)
 * cx_Oracle 5.2.1
 * Oracle 11.2.0.4

The system is a VM on a VmWare vSphere cluster - but the important thing is how much overhead DRCP adds.

The benchmark accessed a single URL on the server that:

 * Does a SELECT on the database by an indexed column
 * Formats an XML file using a Django template

The results are collected using Apache Bench something like this (the URL is modified):

```
ab -n 1000 -c 8 'https://example.com/testing/123'
```

The results are summarized below:


| Test Description | Requests/sec | Mean Response Time (ms) | 50% | 66% | 75% | 80% | 85% | 90% | 98% | 99% | 100% |
| ---------------- | ------------ | ----------------------- | --- | --- | --- | --- | --- | --- | --- | --- | ---- |
| Connection per Request | 35.36  | 226.215                 | 135 | 175 | 305 | 371 | 512 | 560 | 708 | 740 | 1210 |
| Persistent Connection (CONN_MAX_AGE) | 156.32 | 51.178    | 49  | 55  | 60  | 62  | 69  | 71  | 80  |  96 |  269 |
| Connection Pool (django-oracle-drcp) | 139.44 | 57.371    | 56  | 63  | 67  | 70  | 75  | 79  | 87  |  93 |  265 | 

While your results may vary, the point of the numbers above is that Oracle DRCP
and django-oracle-drcp add a minimal amount of overhead while also allowing
multiple applications and application servers to share a pre-allocated number
of connections.


