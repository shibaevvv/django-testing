from http import HTTPStatus

from . import base_test_class as fixtures

OK = HTTPStatus.OK
NOT_FOUND = HTTPStatus.NOT_FOUND
FOUND = HTTPStatus.FOUND


class TestRoutes(fixtures.TestBaseClass):

    def test_pages_availability(self):
        """
        Тест проверяет доступность страниц анонимному пользователю,
        аутентифицированому и автору заметок.
        """
        for url, client_method, expected_status in [
            (fixtures.HOME_URL, self.client.get, OK),
            (fixtures.LOGIN_URL, self.client.get, OK),
            (fixtures.LOGOUT_URL, self.client.post, OK),
            (fixtures.SIGNUP_URL, self.client.get, OK),
            (fixtures.LIST_URL, self.author_client.get, OK),
            (fixtures.ADD_URL, self.author_client.get, OK),
            (fixtures.SUCCESS_URL, self.author_client.get, OK),
            (fixtures.DETAIL_URL, self.author_client.get, OK),
            (fixtures.EDIT_URL, self.author_client.get, OK),
            (fixtures.DELETE_URL, self.author_client.get, OK),
            (fixtures.DETAIL_URL, self.not_author_client.get, NOT_FOUND),
            (fixtures.EDIT_URL, self.not_author_client.get, NOT_FOUND),
            (fixtures.DELETE_URL, self.not_author_client.get, NOT_FOUND),
            (fixtures.LIST_URL, self.client.get, FOUND),
            (fixtures.ADD_URL, self.client.get, FOUND),
            (fixtures.SUCCESS_URL, self.client.get, FOUND),
            (fixtures.DETAIL_URL, self.client.get, FOUND),
            (fixtures.EDIT_URL, self.client.get, FOUND),
            (fixtures.DELETE_URL, self.client.get, FOUND),
        ]:
            with self.subTest(url=url):
                self.assertEqual(
                    client_method(url).status_code, expected_status)

    def test_redirect_for_anonymous_client(self):
        """
        Тестируем редирект анонимного пользователя на страницу для входа,
        если он пытается получить доступ к страницам для
        авторизованных пользователей.
        """
        for url, redirect in [
            [fixtures.LIST_URL, fixtures.REDIRECT_TO_LIST_URL],
            [fixtures.ADD_URL, fixtures.REDIRECT_TO_ADD_URL],
            [fixtures.SUCCESS_URL, fixtures.REDIRECT_TO_SUCCESS_URL],
            [fixtures.DETAIL_URL, fixtures.REDIRECT_TO_DETAIL_URL],
            [fixtures.EDIT_URL, fixtures.REDIRECT_TO_EDIT_URL],
            [fixtures.DELETE_URL, fixtures.REDIRECT_TO_DELETE_URL]
        ]:
            with self.subTest(url=url):
                self.assertRedirects(self.client.get(url), redirect)
