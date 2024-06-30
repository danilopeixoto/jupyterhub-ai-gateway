# Usage

## JupyterHub

Generate service API token:

```console
openssl rand -hex 32
```

Create `jupyterhub_config.py` file:

```python
c.JupyterHub.services = [
    {
        "name": "ai-gateway",
        "url": "http://localhost:8000",
        "api_token": "<service-api-token>"
    }
]

c.JupyterHub.load_roles = [
    {
        "name": "server",
        "scopes": [
            "users:activity!user",
            "access:servers!server",
            "access:services!service=ai-gateway"
        ]
    }
]
```

Start application:

```console
jupyterhub --config jupyterhub_config.py
```

The application will be available at `http://localhost:8888`.

## Service

Set environment variables:

```console
export OPENAI_API_KEY=<openai-api-key>
export JUPYTERHUB_SERVICE_NAME=ai-gateway
export JUPYTERHUB_API_URL=http://localhost:8888/hub/api
export JUPYTERHUB_API_TOKEN=<service-api-token>
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

Start service:

```console
jupyterhub-ai-gateway --config config.yaml
```

The service will be available at `http://localhost:8000`.

Users should be authorized to make requests to the endpoint using the token issued for single-user servers.
