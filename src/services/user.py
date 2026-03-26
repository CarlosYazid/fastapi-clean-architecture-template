from src.repository.abc import Repository
from src.services.abc import BaseService


class UserService(BaseService):
    def __init__(self, user_repository: Repository):
        super().__init__(user_repository)
