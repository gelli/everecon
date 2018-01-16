from everecon import celery_app as app
from celery import task


@app.on_after_finalize.connect
def setup(sender, **kwargs):
    print('setup periodic tasks')
    sender.add_periodic_task(10.0, test_task.s(), name='add every 10')


@task
def test_task():
    print('Hello World')
