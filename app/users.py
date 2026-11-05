# JWT [JSON Web Token] Auth

import uuid

from typing import Optional
from fastapi import Depends, Request
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy
)
from app.database import User, get_user_db
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin, models

