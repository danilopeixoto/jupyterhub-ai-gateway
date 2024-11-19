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
    limit:
        renewal_period: minute
        calls: 10
  - name: chat
    endpoint_type: llm/v1/chat
    model:
        provider: openai
        name: gpt-4-turbo
        config:
            openai_api_key: $OPENAI_API_KEY
    limit:
        renewal_period: minute
        calls: 10
  - name: embeddings
    endpoint_type: llm/v1/embeddings
    model:
        provider: openai
        name: text-embedding-ada-002
        config:
            openai_api_key: $OPENAI_API_KEY
    limit:
        renewal_period: minute
        calls: 10
```

> **Note** For a complete list of supported providers, visit the [MLflow AI Gateway](https://mlflow.org/docs/latest/llms/deployments/index.html#supported-provider-models) documentation.

Start service:

```console
jupyterhub-ai-gateway --config config.yaml
```

The service will be available at `http://localhost:5000`.

## Hub

Create `jupyterhub_config.py` file:

```python
c.JupyterHub.services = [
    {
        "name": "ai-gateway",
        "api_token": "<service-api-token>",
        "oauth_redirect_uri": "http://localhost:5000/oauth_callback",
        "oauth_client_allowed_scopes": [
            "access:services!service=ai-gateway",
            "custom:ai-gateway:full-access",
        ],
        "display": False,
    }
]

c.JupyterHub.custom_scopes = {
    "custom:ai-gateway:full-access": {
        "description": "Full access to AI gateway service.",
    },
}

c.JupyterHub.load_roles = [
    {
        "name": "user",
        "scopes": [
            "self",
            "access:services!service=ai-gateway",
            "custom:ai-gateway:full-access",
        ]
    },
    {
        "name": "server",
        "scopes": [
            "users:activity!user",
            "access:servers!server",
            "access:services!service=ai-gateway",
            "custom:ai-gateway:full-access",
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

Users should be authorized to make requests to `http://localhost:5000` service using the token issued for single-user servers.

## Single-user server

Install dependencies:

```console
pip install openai
```

Send completion requests:

```python
import os

from openai import OpenAI


client = OpenAI(
    base_url="http://localhost:5000/v1",
    api_key=os.environ["JUPYTERHUB_API_TOKEN"],
)

completion = client.completions.create(
    model="completions", # endpoint name
    prompt="The quick brown fox...",
    max_tokens=64,
)

print(completion.choices[0].text)
```

> **Note** For a complete list of supported endpoints, access the service API documentation at `http://localhost:5000/docs`.
