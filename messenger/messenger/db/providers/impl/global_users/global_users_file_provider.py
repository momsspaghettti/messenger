import os
from typing import Optional, List, Dict
from messenger.db.providers.global_users_provider import GlobalUsersProvider
from messenger.models.common.global_user import GlobalUser
from messenger.project_path import PROJECT_PATH


class GlobalUsersFileProvider(GlobalUsersProvider):
    def __init__(self, file_name):
        self.file_name = os.path.join(PROJECT_PATH, file_name)
        self.global_users: Dict[str, GlobalUser] = {}
        self.in_cache = False

    async def save_users(self, users: List[GlobalUser]) -> None:
        self.in_cache = False
        self.global_users = {}
        with open(self.file_name, 'a') as file:
            for user in users:
                file.write(f'{user.login};{user.name};{user.utc_offset}\n')

    async def get_user(self, login: str) -> Optional[GlobalUser]:
        if not self.in_cache:
            self.global_users = {}
            self.fill_cache()
            self.in_cache = True
        if login not in self.global_users:
            return None
        return self.global_users[login]

    def fill_cache(self):
        with open(self.file_name, 'r') as file:
            for line in file:
                if line is None or line == '':
                    continue
                line_arr = line.split(';')
                user = GlobalUser(id_=line_arr[0], login=line_arr[1], name=line_arr[2], utc_offset=line_arr[3])
                self.global_users[user.login] = user
