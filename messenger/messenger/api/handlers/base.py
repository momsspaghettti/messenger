import json
import logging
from aiohttp.web_urldispatcher import View
from aiohttp import web
from pydantic import ValidationError
from messenger.models.responses.errors.bad_default import DefaultErrorResponse
from messenger.models.responses.errors.bad_params import BadParametersResponse
from messenger.models.responses.base import BaseResponse
from messenger.models.requests.base import BaseRequest
from typing import Type, Optional
from abc import ABCMeta, abstractmethod
from aiopg.sa.engine import Engine
from messenger.models.common.global_user import GlobalUser
from messenger.models.responses.errors.base import BaseErrorResponse
from messenger.utils.db import is_db_available
from messenger.utils.timer import Timer, TimerErrorSignal
from psycopg2.errors import InvalidTextRepresentation
from messenger.db.schema import (
    users_sessions_table as sessions_tbl,
    global_users_table as global_users_tbl)
from sqlalchemy import select
from messenger.models.responses.errors.unauthorized import UnauthorizedErrorResponse


class Handler(View):
    URL_PATH: str


class BaseView(Handler, metaclass=ABCMeta):
    @property
    def db(self) -> Engine:
        return self.request.app['db']

    def get_logger(self, name) -> logging.Logger:
        return self.request.app['logger_factory'].get_logger(name)

    async def handle_request(self, request_cls: Type[BaseRequest]) -> web.Response:
        """
        Base method for handle and middleware request
        :param request_cls: Type of request object
        :return: HttpResponse
        """

        logger = self.get_logger(__name__)

        response: BaseResponse
        err = None
        try:
            error_signal = TimerErrorSignal()
            with Timer(logger, f'Handle endpoint {self.request}', error_signal):
                db_available = await is_db_available(self.request.app)

                if not db_available:
                    logger.warning('Database is unavailable')
                else:
                    logger.info('Database is available')

                authenticated, user = await self.auth_and_get_user(db_available)

                if not authenticated:
                    logger.warning('Failed to auth request')
                    response = UnauthorizedErrorResponse(message='failed to auth by given session_id')
                else:
                    if not db_available and not self.can_process_request_without_db:
                        response = DefaultErrorResponse(message='Database is unavailable')
                    else:
                        request = await self.build_request(request_cls)
                        response = await self.process_request(request, user, db_available)

                if isinstance(response, BaseErrorResponse):
                    error_signal.error = True
        except (ValidationError, ValueError, TypeError, InvalidTextRepresentation) as e:
            err = e
            response = BadParametersResponse()
        except Exception as e:
            err = e
            response = DefaultErrorResponse()
        finally:
            if err is not None:
                logger.exception(err)

        logger.info('\nResponse:\n{}\n'.format(response.json()))
        return response.to_web_response()

    async def auth_and_get_user(self, db_available: bool) -> (bool, Optional[GlobalUser]):
        logger = self.get_logger(__name__)

        if not db_available or not self.need_to_auth:
            return True, None

        session_id = self.request.headers['X-Auth-Token'] if 'X-Auth-Token' in self.request.headers else ''

        user_session_query = select(
            sessions_tbl.c.session_id,
            global_users_tbl.c.id,
            global_users_tbl.c.login,
            global_users_tbl.c.name,
            global_users_tbl.c.utc_offset
        ) \
            .outerjoin(
            global_users_tbl,
            sessions_tbl.c.global_user_id == global_users_tbl.c.id) \
            .where(sessions_tbl.c.session_id == session_id)

        async with self.db.acquire() as conn:
            async with conn.begin():
                user_session_select = await conn.execute(
                    user_session_query
                )

                if user_session_select.rowcount != 1:
                    logger.warning(f'User with session_id = {session_id} not found')
                    return False, None

                user_session = await user_session_select.fetchone()

                return True, GlobalUser(
                    id=user_session['id'],
                    session_id=user_session['session_id'],
                    login=user_session['login'],
                    name=user_session['name'],
                    utc_offset=user_session['utc_offset'])

    async def build_request(self, request_cls: Type[BaseRequest]) -> BaseRequest:
        logger = self.get_logger(__name__)

        body_obj = json.loads(await self.request.read()) if self.request.body_exists else {}

        logger.info('\nRequest:\nPath: {}\nQuery: {}\nBody: {}\n'.format(
            json.dumps({**self.request.match_info}),
            json.dumps({**self.request.rel_url.query}),
            json.dumps({**body_obj})
        ))

        return request_cls(
            **self.request.match_info,
            **self.request.rel_url.query,
            **body_obj)

    @abstractmethod
    async def process_request(
            self,
            request: BaseRequest,
            user: Optional[GlobalUser],
            db_available: bool) -> BaseResponse:
        raise NotImplementedError('abstract method')

    @property
    @abstractmethod
    def need_to_auth(self) -> bool:
        raise NotImplementedError('abstract method')

    @property
    @abstractmethod
    def can_process_request_without_db(self) -> bool:
        raise NotImplementedError('abstract method')
