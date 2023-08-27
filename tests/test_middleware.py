import dataclasses
import logging
from typing import Any

import pytest
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from pydantic import BaseModel
from typing_extensions import TypedDict

from fastapi_mock_middleware import MockAPIMiddleware, APINotImplementedError

logger = logging.getLogger(__name__)


@pytest.fixture
def app() -> FastAPI:
    app = FastAPI()
    app.add_middleware(MockAPIMiddleware)
    return app


@pytest.fixture
async def client(app: FastAPI) -> AsyncClient:
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url='http://testserver',
    ) as client:
        yield client


class ExampleSchema(BaseModel):
    message: str


class ExampleTypedDict(TypedDict):
    message: str


@dataclasses.dataclass
class ExampleDataclass:
    message: str


async def test_not_mocked(client, app) -> None:
    @app.get('/')
    async def view() -> ExampleSchema:
        return ExampleSchema(message='not mocked')  # <--

    r = await client.get('/')
    assert r.status_code == 200
    assert r.json() == {'message': 'not mocked'}


async def test_with_return_type(client, app) -> None:  # uses return type of function
    @app.get('/')
    async def view() -> ExampleSchema:  # <--
        raise APINotImplementedError()

    r = await client.get('/')
    assert r.status_code == 200
    data = r.json()
    assert data.get('message')


async def test_with_response_model(client, app) -> None:
    @app.get('/', response_model=ExampleSchema)  # <--
    async def view():
        raise APINotImplementedError()

    r = await client.get('/')
    assert r.status_code == 200
    data = r.json()
    assert data.get('message')


async def test_raising_with_return_value(client, app) -> None:
    @app.get('/')
    async def view():
        raise APINotImplementedError(
            return_value={'message': 'raised with the specified return value'}  # <--
        )

    r = await client.get('/')
    assert r.status_code == 200
    assert r.json() == {'message': 'raised with the specified return value'}


@pytest.mark.parametrize(
    'response_model, assert_fn', [
        (None, lambda data: data is None),
        (Any, lambda data: data == {}),
        (str, lambda data: data),
        (ExampleSchema, lambda data: data.get('message')),
        (ExampleTypedDict, lambda data: data.get('message')),
        (ExampleDataclass, lambda data: data.get('message')),
        (list[ExampleSchema], lambda data: (data and data[0].get('message'))),
        (list[str], lambda data: (data and data[0])),
        (dict[str, ExampleSchema], lambda data: (data and data.get('', {}).get('message'))),
        (dict[str, str], lambda data: data),
    ]
)
async def test_response_models(client, app, response_model, assert_fn) -> None:
    @app.get('/', response_model=response_model)
    async def view():
        raise APINotImplementedError()

    r = await client.get('/')
    assert r.status_code == 200
    data = r.json()
    assert assert_fn(data), f'{response_model} -> {data}'


@pytest.mark.parametrize(
    'response_model', [
        object,
    ]
)
async def test_reraise_on_unable_to_mock(client, app, response_model) -> None:
    @app.get('/', response_model=response_model)
    async def view():
        raise APINotImplementedError()

    with pytest.raises(APINotImplementedError):
        r = await client.get('/')
