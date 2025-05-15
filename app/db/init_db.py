import os
import sys

from app.db.session import engine
from app.models import Base
from app.models.notification import Notification  # noqa: F401
from app.models.user import User  # noqa: F401

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "../../",
        )
    )
)


def init():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init()
