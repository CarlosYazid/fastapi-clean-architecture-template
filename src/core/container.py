from dependency_injector import containers, providers

from core.settings import get_settings
from core.database import Database
from repository import UserRepository
from services import AuthService, UserService
from util.auth import AuthUtils


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "api.v1.endpoints.auth",
            "api.v1.endpoints.user",
            "core.dependencies",
        ]
    )

    db = providers.Singleton(Database, db_url=get_settings().DATABASE_URI)

    auth_utils = providers.Factory(AuthUtils, settings=get_settings())

    user_repository = providers.Factory(
        UserRepository, session_factory=db.provided.session
    )

    auth_service = providers.Factory(AuthService, user_repository=user_repository)
    user_service = providers.Factory(UserService, user_repository=user_repository)
