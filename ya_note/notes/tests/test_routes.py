from http import HTTPStatus

from . import base_test_class as cfg

OK = HTTPStatus.OK
NOT_FOUND = HTTPStatus.NOT_FOUND
FOUND = HTTPStatus.FOUND


class TestRoutes(cfg.TestBaseClass):

    def test_pages_availability(self):
        """
        Тест проверяет доступность страниц анонимному пользователю,
        аутентифицированому и автору заметок.
        """
        for url, client_method, expected_status in [
            (cfg.URL_HOME, self.client.get, OK),
            (cfg.URL_LOGIN, self.client.get, OK),
            (cfg.URL_LOGOUT, self.client.post, OK),
            (cfg.URL_SIGNUP, self.client.get, OK),
            (cfg.URL_LIST, self.author_client.get, OK),
            (cfg.URL_ADD, self.author_client.get, OK),
            (cfg.URL_SUCCESS, self.author_client.get, OK),
            (cfg.URL_DETAIL, self.author_client.get, OK),
            (cfg.URL_EDIT, self.author_client.get, OK),
            (cfg.URL_DELETE, self.author_client.get, OK),
            (cfg.URL_DETAIL, self.not_author_client.get, NOT_FOUND),
            (cfg.URL_EDIT, self.not_author_client.get, NOT_FOUND),
            (cfg.URL_DELETE, self.not_author_client.get, NOT_FOUND),
            (cfg.URL_LIST, self.client.get, FOUND),
            (cfg.URL_ADD, self.client.get, FOUND),
            (cfg.URL_SUCCESS, self.client.get, FOUND),
            (cfg.URL_DETAIL, self.client.get, FOUND),
            (cfg.URL_EDIT, self.client.get, FOUND),
            (cfg.URL_DELETE, self.client.get, FOUND),
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
            [cfg.URL_LIST, cfg.URL_REDIRECT_LIST],
            [cfg.URL_ADD, cfg.URL_REDIRECT_ADD],
            [cfg.URL_SUCCESS, cfg.URL_REDIRECT_SUCCESS],
            [cfg.URL_DETAIL, cfg.URL_REDIRECT_DETAIL],
            [cfg.URL_EDIT, cfg.URL_REDIRECT_EDIT],
            [cfg.URL_DELETE, cfg.URL_REDIRECT_DELETE]
        ]:
            with self.subTest(url=url):
                self.assertRedirects(self.client.get(url), redirect)
