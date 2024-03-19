# FastAPI mock middleware

[![license](https://img.shields.io/badge/License-MIT-dark)](https://github.com/NiyazNz/fastapi-mock-middleware/blob/main/LICENSE.txt)
[![pypi](https://img.shields.io/pypi/v/fastapi-mock-middleware?color=00FF00)](https://pypi.org/project/fastapi-mock-middleware/)
[![test](https://github.com/NiyazNz/fastapi-mock-middleware/workflows/Test/badge.svg)](https://github.com/NiyazNz/fastapi-mock-middleware/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/NiyazNz/fastapi-mock-middleware/graph/badge.svg?token=GX8A8HD0KL)](https://codecov.io/gh/NiyazNz/fastapi-mock-middleware)

FastAPI middleware for mocking response data of non-implemented endpoints.

Mock data is generated in accordance with endpoint return type or provided
response_model using [polifactory](https://github.com/litestar-org/polyfactory).

---

For more information on how to use fastapi-mock-middleware, please refer to the
[official documentation](https://niyaznz.github.io/fastapi-mock-middleware/).

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
