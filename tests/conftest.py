import os
import sys
from unittest.mock import patch

import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


@pytest.fixture(autouse=True)
def mock_celery_delay():
    # 실제 Redis나 Celery 연결 없이 send_notification.delay() 호출을 무시함
    with patch("app.tasks.notify.send_notification.delay") as mock:
        yield mock
