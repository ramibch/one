# django-project-template


## Conventions

### tasks.py

* Standard Task: `<do_something>_task`
* Periodic tasks:
  * Weekly task: `<do_something>_weekly`
  * Dairly task: `<do_something>_darily`
  * Hourly task: `<do_something>_hourly`
  * Every X minutes Task : `<do_something>_every_X_min`






## Submodules

[https://gist.github.com/gitaarik/8735255](https://gist.github.com/gitaarik/8735255)


## How-tos

## Create a new database in Postgres

```shell
sudo -u postgres psql
```

```shell
CREATE DATABASE mydata_db;
CREATE USER my_db_user WITH PASSWORD 'Secure-Password-Here';
ALTER ROLE my_db_user SET client_encoding TO 'utf8';
ALTER ROLE my_db_user SET timezone TO 'UTC';
ALTER ROLE my_db_user SET default_transaction_isolation TO 'read committed';
GRANT ALL PRIVILEGES ON DATABASE mydata_db TO my_db_user;

```
