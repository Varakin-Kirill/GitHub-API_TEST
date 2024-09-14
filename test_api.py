from dotenv import load_dotenv
import os
import requests
import pytest


@pytest.fixture()
def init():
    load_dotenv()
    token = os.getenv("GITHUB_TOKEN")
    user_name = os.getenv("USER_NAME")
    repository_name = os.getenv("REPOSITORY_NAME")
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }
    data = {
        "name": repository_name,
        "description": "",
        "private": False,
    }
    return user_name, repository_name, headers, data


def test_repo(init):
    user_name, repository_name, headers, data = init

    # создание репозитория
    response = requests.post(
        "https://api.github.com/user/repos", headers=headers, json=data
    )
    assert (
        response.status_code == 201
    ), f"Expected status code 201 Created, but got {response.status_code}. Response: {response.text}"

    # проверить создан ли репозиторий
    response = requests.get("https://api.github.com/user/repos", headers=headers).json()
    repo_names = [repo["name"] for repo in response]
    assert (
        repository_name in repo_names
    ), f"Repository '{repository_name}' was not found in the list of repositories. Repositories: {repo_names}"

    # удаление репозитория
    response = requests.delete(
        f"https://api.github.com/repos/{user_name}/{repository_name}",
        headers=headers,
    )
    assert (
        response.status_code == 204
    ), f"Expected status code 204 No Content, but got {response.status_code}. Response: {response.text}"
    response = requests.get(
        f"https://api.github.com/repos/{user_name}/{repository_name}", headers=headers
    )
    assert (
        response.status_code == 404
    ), f"Expected status code 404 Not Found, but got {response.status_code}. Response: {response.text}"
