# fastapi-tortoise-poetry-template
![Python Versions](https://img.shields.io/pypi/pyversions/asynctor)
![Mypy coverage](https://img.shields.io/badge/mypy-100%25-green.svg)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![CI](https://github.com/waketzheng/fastapi-tortoise-poetry-template/workflows/ci/badge.svg)](https://github.com/waketzheng/fastapi-tortoise-poetry-template/actions?query=workflow:ci)

Template for python backend project using FastAPI+TortoiseORM+poetry+aerich

Inspired by [full-stack-fastapi-template](https://github.com/fastapi/full-stack-fastapi-template)

## Technology Stack and Features

- ⚡ [**FastAPI**](https://fastapi.tiangolo.com) for the Python backend API.
  - 🧰 [TortoiseORM](https://tortoise.github.io) for the Python SQL database interactions (ORM).
  - 🔍 [Pydantic](https://docs.pydantic.dev), used by FastAPI, for the data validation and settings management.
- ✅ Tests with [Pytest](https://pytest.org).

## Quickstart

```bash
poetry shell
poetry install
# For MySQL: poetry install -E mysql
# For PostgreSQL: poetry install -E postgres
aerich init-db
python app.py
```

## How To Use It

You can **just fork or clone** this repository and use it as is.

✨ It just works. ✨

### How to Use a Private Repository

If you want to have a private repository, GitHub won't allow you to simply fork it as it doesn't allow changing the visibility of forks.

But you can do the following:

- Create a new GitHub repo, for example `my-backend-project`.
- Clone this repository manually, set the name with the name of the project you want to use, for example `my-backend-project`:

```bash
git clone git@github.com:waketzheng/fastapi-tortoise-poetry-template.git my-backend-project
```

- Enter into the new directory:

```bash
cd my-backend-project
```

- Set the new origin to your new repository, copy it from the GitHub interface, for example:

```bash
git remote set-url origin git@github.com:octocat/my-backend-project.git
```

- Add this repo as another "remote" to allow you to get updates later:

```bash
git remote add upstream git@github.com:waketzheng/fastapi-tortoise-poetry-template.git
```

- Push the code to your new repository:

```bash
git push -u origin master
```
