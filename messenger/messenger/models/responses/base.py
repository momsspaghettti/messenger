from messenger.models.base import MyBaseModel
from aiohttp.web_response import Response


class BaseResponse(MyBaseModel):
    status_code: int

    def to_web_response(self) -> Response:
        return Response(status=self.status_code, content_type='application/json', body=self.get_response_data())

    def get_response_data(self) -> str:
        return self.json(exclude={'status_code'})
