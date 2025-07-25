from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects

pytestmark = pytest.mark.django_db

OK = HTTPStatus.OK
NOT_FOUND = HTTPStatus.NOT_FOUND
FOUND = HTTPStatus.FOUND

CLIENT = pytest.lazy_fixture('client')
AUTHOR = pytest.lazy_fixture('author_client')
NOT_AUTHOR = pytest.lazy_fixture('not_author_client')

HOME_URL = pytest.lazy_fixture('home_url')
NEWS_DETAIL_URL = pytest.lazy_fixture('news_detail_url')
LOGIN_URL = pytest.lazy_fixture('login_url')
LOGOUT_URL = pytest.lazy_fixture('logout_url')
SIGNUP_URL = pytest.lazy_fixture('signup_url')
COMMENT_EDIT_URL = pytest.lazy_fixture('edit_comment_url')
COMMENT_DELETE_URL = pytest.lazy_fixture('delete_comment_url')

REDIRECT_TO_COMMENT_EDIT_URL = pytest.lazy_fixture(
    'redirect_to_comment_edit_url')
REDIRECT_TO_COMMENT_DELETE_URL = pytest.lazy_fixture(
    'redirect_to_comment_delete_url'
)


@pytest.mark.parametrize(
    'url, parametrized_client, expected_status',
    (
        (HOME_URL, CLIENT, OK),
        (NEWS_DETAIL_URL, CLIENT, OK),
        (LOGIN_URL, CLIENT, OK),
        (LOGOUT_URL, CLIENT, OK),
        (SIGNUP_URL, CLIENT, OK),
        (COMMENT_EDIT_URL, AUTHOR, OK),
        (COMMENT_DELETE_URL, NOT_AUTHOR, NOT_FOUND),
        (COMMENT_EDIT_URL, AUTHOR, OK),
        (COMMENT_DELETE_URL, NOT_AUTHOR, NOT_FOUND),
        (COMMENT_EDIT_URL, CLIENT, FOUND),
        (COMMENT_DELETE_URL, CLIENT, FOUND),
    )
)
def test_pages_availability_for_anonymous_user(url, parametrized_client,
                                               expected_status, logout_url):
    """
    Проверка доступности страниц для анонимного пользователя:
    главная, отдельной новости, регистрации пользователей, входа в
    учётную запись и выхода из неё.
    """
    request_type = parametrized_client.post if url == logout_url else (
        parametrized_client.get
    )
    assert request_type(url).status_code == expected_status


@pytest.mark.parametrize(
    'url, redirect_to', (
        (COMMENT_EDIT_URL, REDIRECT_TO_COMMENT_EDIT_URL),
        (COMMENT_DELETE_URL, REDIRECT_TO_COMMENT_DELETE_URL)
    )
)
def test_redirects(client, url, redirect_to):
    """
    Проверка перенаправления анонимного пользователя на страницу
    авторизации при попытке зайти на страницу редактирования или удаления
    комментария.
    """
    assertRedirects(client.get(url), redirect_to)
