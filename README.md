# Django Migration City Resource

> Resource: https://github.com/simphyF/citySql
> Migration Issues: https://gist.github.com/devhero/22c702fea284b3eaed3a3d643bd20b17

1. Resolve regional cities in the world, json format with django migrations.

2. Django migration wil not reset postgres' primary key sequence

- option 1: Don't set pk field in migration

- option 2: Reset sequence every time update or create new db data

```python
from django.db import connection

def idseq(model_class):
    return '{}_id_seq'.format(model_class._meta.db_table)

def reset_sequence(model_class, value=1):
    cursor = connection.cursor()
    sequence = idseq(model_class)
    cursor.execute("ALTER SEQUENCE {} RESTART WITH {};".format(sequence, value))
    cursor.close()
```
