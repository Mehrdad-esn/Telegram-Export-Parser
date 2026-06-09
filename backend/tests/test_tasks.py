from backend.worker import celery_app
from backend.app.tasks import process_export_task


def test_can_queue_task():
    """Ensure the Celery task is registered and can be invoked.

    We use task_always_eager=True so the task runs synchronously in the test
    process (no broker required). This verifies registration and basic behavior
    without requiring a running Redis instance.
    """
    celery_app.conf.update(task_always_eager=True)

    payload = {
        "messages": [
            {
                "id": 1,
                "date": "2020-01-01",
                "type": "message",
                "from": "A",
                "text": "hi",
            }
        ]
    }

    async_result = process_export_task.delay(payload)
    result = async_result.get(timeout=5)

    assert result == {
        "processed": True,
        "chats": [{"name": "Unnamed chat", "messages": ["[2020-01-01] A\nhi"]}],
    }
