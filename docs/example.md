Let's assume that we have designed the following API:

```Python
{!example_unmocked.py!}
```

We have prepared endpoints, described filters, chosen pagination methods, and
defined the input and output data formats, but implementation is not yet ready.
After the server starts, we can see the OpenAPI schema and the UI for it
at <http://127.0.0.1:8000/docs/>. We can share the schema of our API with other
teams so that they can start doing their part of the work while we implement the
internal logic of our application in parallel. But there's a small problem: when
we make a request to our API, it responds with an error, meaning it's not quite
ready to use.

Let's have a look at the solution!

## Configure mocking

Add `MockAPIMiddleware` middleware to app and raise `APINotImplementedError`
in your endpoint stubs.

```Python hl_lines="8 22 27 32 37 42"
{!example.py!}
```

## Check it

Open your browser at <http://127.0.0.1:8000/docs> and try to call API using
Swagger UI or use `curl`. All called APIs must return mocked data as a response.

- Get list:

```shell
curl http://127.0.0.1:8000/
```

- Get one:

```shell
curl http://127.0.0.1:8000/1/
```

- Create:

```shell
curl -X POST http://127.0.0.1:8000/ -H 'Content-Type: application/json' -d '{
  "name": "string"
}'

```

- Update:

```shell
curl -X PUT http://127.0.0.1:8000/1/ -H 'Content-Type: application/json' -d '{
  "id": 1,
  "name": "string"
}'

```

- Delete

```shell
curl -X DELETE -v http://127.0.0.1:8000/1/
```
