from django.contrib.auth.models import AbstractUser
from django.db.models.query import ValuesIterable
from typing import Any

type UserModelValuesQueryset = ValuesIterable[AbstractUser, dict[str, Any]]
