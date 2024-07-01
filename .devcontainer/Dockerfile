FROM python:3.10-buster

RUN groupadd --gid 1000 developer \
    && useradd --uid 1000 --gid developer --shell /bin/bash --create-home developer

WORKDIR /workspaces/jupyterhub-ai-gateway
