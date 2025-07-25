from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects

pytestmark = pytest.mark.django_db

CLIENT = pytest.lazy_fixture('client')
AUTHOR = pytest.lazy_fixture('author_client')
NOT_AUTHOR = pytest.lazy_fixture('not_author_client')

URL_HOME = pytest.lazy_fixture('url_home')
URL_NEWS_DETAIL = pytest.lazy_fixture('url_news_detail')
URL_LOGIN = pytest.lazy_fixture('url_login')
URL_LOGOUT = pytest.lazy_fixture('url_logout')
URL_SIGNUP = pytest.lazy_fixture('url_signup')
URL_COMMENT_EDIT = pytest.lazy_fixture('url_edit_comment')
URL_COMMENT_DELETE = pytest.lazy_fixture('url_delete_comment')

URL_REDIRECT_COMMENT_EDIT = pytest.lazy_fixture('redirect_comment_edit')
URL_REDIRECT_COMMENT_DELETE = pytest.lazy_fixture('redirect_comment_delete')


@pytest.mark.parametrize(
    'url, parametrized_client, expected_status',
    (
        (URL_HOME, CLIENT, HTTPStatus.OK),
        (URL_NEWS_DETAIL, CLIENT, HTTPStatus.OK),
        (URL_LOGIN, CLIENT, HTTPStatus.OK),
        (URL_LOGOUT, CLIENT, HTTPStatus.OK),
        (URL_SIGNUP, CLIENT, HTTPStatus.OK),
        (URL_COMMENT_EDIT, AUTHOR, HTTPStatus.OK),
        (URL_COMMENT_DELETE, NOT_AUTHOR, HTTPStatus.NOT_FOUND),
        (URL_COMMENT_EDIT, AUTHOR, HTTPStatus.OK),
        (URL_COMMENT_DELETE, NOT_AUTHOR, HTTPStatus.NOT_FOUND),
    )
)
def test_pages_availability_for_anonymous_user(url, parametrized_client,
                                               expected_status, url_logout):
    """
    Проверка доступности страниц для анонимного пользователя:
    главная, отдельной новости, регистрации пользователей, входа в
    учётную запись и выхода из неё.
    """
    request_type = parametrized_client.post if url == url_logout else (
        parametrized_client.get
    )
    assert request_type(url).status_code == expected_status


@pytest.mark.parametrize(
    'url, redirect_to', (
        (URL_COMMENT_EDIT, URL_REDIRECT_COMMENT_EDIT),
        (URL_COMMENT_DELETE, URL_REDIRECT_COMMENT_DELETE)
    )
)
def test_redirects(client, url, redirect_to):
    """
    Проверка перенаправления анонимного пользователя на страницу
    авторизации при попытке зайти на страницу редактирования или удаления
    комментария.
    """
    assertRedirects(client.get(url), redirect_to)
