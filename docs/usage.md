# Usage

## Service

Generate service API token:

```console
openssl rand -hex 32
```

Set environment variables:

```console
export OPENAI_API_KEY=<openai-api-key>
export JUPYTERHUB_API_URL=http://localhost:8000/hub/api
export JUPYTERHUB_API_TOKEN=<service-api-token>
export JUPYTERHUB_PUBLIC_URL=http://localhost:5000
export JUPYTERHUB_PUBLIC_HUB_URL=http://localhost:8000
```

Create `config.yaml` file:

```yaml
endpoints:
  - name: completions
    endpoint_type: llm/v1/completions
    model:
        provider: openai
        name: gpt-4-turbo
        config:
            openai_api_key: $OPENAI_API_KEY
  - name: chat
    endpoint_type: llm/v1/chat
    model:
        provider: openai
        name: gpt-4-turbo
        config:
            openai_api_key: $OPENAI_API_KEY
  - name: embeddings
    endpoint_type: llm/v1/embeddings
    model:
        provider: openai
        name: text-embedding-ada-002
        config:
            openai_api_key: $OPENAI_API_KEY
```

> **Note** For a complete list of supported providers, visit the [MLflow Deployments Server](https://mlflow.org/docs/latest/llms/deployments/index.html#supported-provider-models) documentation.

Start service:

```console
jupyterhub-ai-gateway --config config.yaml
```

The service will be available at `http://localhost:5000/services/ai-gateway`.

## Hub

Create `jupyterhub_config.py` file:

```python
c.JupyterHub.services = [
    {
        "name": "ai-gateway",
        "api_token": "<service-api-token>",
        "oauth_redirect_uri": "http://localhost:5000/services/ai-gateway/oauth_callback",
        "display": False
    }
]

c.JupyterHub.load_roles = [
    {
        "name": "user",
        "scopes": [
            "self",
            "access:services!service=ai-gateway",
        ]
    },
    {
        "name": "server",
        "scopes": [
            "users:activity!user",
            "access:servers!server",
            "access:services!service=ai-gateway",
        ]
    },
]

c.JupyterHub.authenticator_class = "dummy"
c.JupyterHub.spawner_class = "simple"
```

Start application:

```console
jupyterhub --config jupyterhub_config.py
```

The application will be available at `http://localhost:8000`.

Users should be authorized to make requests to `http://localhost:5000/services/ai-gateway` service using the token issued for single-user servers.

## Client

Send completion requests:

```python
import asyncio

import httpx


async def main():
    url = "http://localhost:5000/services/ai-gateway/v1/completions"
    headers = {
        "Authorization": "Bearer <token>",
    }

    data = {
        "model": "completions", # endpoint name
        "prompt": "The quick brown fox...",
        "max_tokens": 64,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=data)
        response.raise_for_status()

        print(response.json())


if __name__ == "__main__":
   asyncio.run(main())
```

> **Note** For a complete list of supported endpoints, access the service API documentation at `http://localhost:5000/services/ai-gateway/docs`.
