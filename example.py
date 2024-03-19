import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from fastapi_mock_middleware import MockAPIMiddleware, APINotImplementedError

app = FastAPI()
app.add_middleware(MockAPIMiddleware)


class Item(BaseModel):
    id: int
    name: str


class CreateItem(BaseModel):
    name: str


@app.get('/')
async def list_items(offset: int = 0, limit: int = 20, q: str = None) -> list[Item]:
    raise APINotImplementedError()


@app.post('/', status_code=201)
async def create_item(*, item_in: CreateItem) -> Item:
    raise APINotImplementedError()


@app.get('/{uid}/')
async def get_item(*, uid: int) -> Item:
    raise APINotImplementedError()


@app.put('/{uid}/')
async def update_item(*, uid: int, item_in: Item) -> Item:
    raise APINotImplementedError()


@app.delete('/{uid}/', status_code=204)
async def delete_item(*, uid: int) -> None:
    raise APINotImplementedError()


if __name__ == '__main__':
    uvicorn.run('example:app', reload=True)
