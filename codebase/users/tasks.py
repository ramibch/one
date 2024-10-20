from huey import crontab
from huey.contrib import djhuey as huey


@huey.db_periodic_task(crontab(hour="0", minute="1"))
def example_task_dairly():
    pass
