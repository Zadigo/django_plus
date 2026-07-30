from typing import Any

from django.contrib.auth.models import AbstractUser
from django.db.models.query import ValuesIterable

type UserModelValuesQueryset = ValuesIterable[AbstractUser, dict[str, Any]]
