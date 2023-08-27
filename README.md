# FastAPI mock middleware

FastAPI middleware for mocking response data of non-implemented endpoints.

Mock data is generated in accordance with endpoint return type or provided
response_model using [polifactory](https://github.com/litestar-org/polyfactory).

## Installation

```shell
pip install fastapi-mock-middleware
```

## Usage example

Add `MockAPIMiddleware` middleware to app and raise `APINotImplementedError` in
your endpoint stubs.

```Python hl_lines="8 18"
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from fastapi_mock_middleware import MockAPIMiddleware, APINotImplementedError

app = FastAPI()
app.add_middleware(MockAPIMiddleware)


class Item(BaseModel):
    id: int
    name: str


@app.get('/')
async def list_items() -> list[Item]:
    raise APINotImplementedError()


if __name__ == '__main__':
    uvicorn.run('example:app', reload=True)
```

Check the response using `curl`.

```shell
curl http://127.0.0.1:8000/
```

Called API must return mocked data:

```json
[
  {
    "id": 5392,
    "name": "gVzyVVUmGGevXlQvXGBW"
  }
]
```
