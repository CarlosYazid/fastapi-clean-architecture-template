from dependency_injector import containers, providers

from src.core.settings import get_settings
from src.core.database import Database
from src.repository import UserRepository
from src.services import AuthService, UserService
from src.util.auth import AuthUtils


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.api.v1.endpoints.auth",
            "src.api.v1.endpoints.user",
            "src.core.dependencies",
        ]
    )

    db = providers.Singleton(Database, db_url=get_settings().DATABASE_URI)

    auth_utils = providers.Factory(AuthUtils, settings=get_settings())

    user_repository = providers.Factory(UserRepository, session_factory=db.provided.session)

    auth_service = providers.Factory(AuthService, user_repository=user_repository)
    user_service = providers.Factory(UserService, user_repository=user_repository)
