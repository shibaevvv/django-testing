from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects
from pytest_lazyfixture import lazy_fixture


@pytest.mark.django_db
@pytest.mark.parametrize(
    'url',
    (
        lazy_fixture('url_home'),
        lazy_fixture('url_news_detail'),
        lazy_fixture('url_login'),
        lazy_fixture('url_logout'),
        lazy_fixture('url_signup'),
    )
)
def test_pages_availability_for_anonymous_user(client, url, url_logout):
    """
    Проверка доступности страниц для анонимного пользователя:
    главная, отдельной новости, регистрации пользователей, входа в
    учётную запись и выхода из неё.
    """
    request_type = client.post if url == url_logout else client.get
    assert request_type(url).status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    [
        (lazy_fixture('not_author_client'), HTTPStatus.NOT_FOUND),
        (lazy_fixture('author_client'), HTTPStatus.OK)
    ],
)
@pytest.mark.parametrize(
    'url',
    (lazy_fixture('url_edit_comment'), lazy_fixture('url_delete_comment'),)
)
def test_pages_availability_for_different_users(
        parametrized_client, expected_status, url
):
    """
    Проверка, что страницы удаления и редактирования комментария доступны
    автору комментария. Авторизованный пользователь не может зайти на
    страницы редактирования или удаления чужих комментариев (возвращается
    ошибка 404).
    """
    assert parametrized_client.get(url).status_code == expected_status


@pytest.mark.parametrize(
    'url',
    (lazy_fixture('url_edit_comment'), lazy_fixture('url_delete_comment'),)
)
def test_redirects(client, url, url_login):
    """
    Проверка перенаправления анонимного пользователя на страницу
    авторизации при попытке зайти на страницу редактирования или удаления
    комментария.
    """
    assertRedirects(client.get(url), f'{url_login}?next={url}')
