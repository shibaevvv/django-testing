from http import HTTPStatus

from .base_test_class import TestBaseClass


class TestRoutes(TestBaseClass):

    def test_pages_availability(self):
        """
        Тест проверяет доступность страниц анонимному пользователю,
        аутентифицированому и автору заметок.
        """
        urls = (
            (self.urls['home'], self.client, HTTPStatus.OK),
            (self.urls['login'], self.client, HTTPStatus.OK),
            (self.urls['logout'], self.client, HTTPStatus.OK),
            (self.urls['signup'], self.client, HTTPStatus.OK),
            (self.urls['list'], self.author_client, HTTPStatus.OK),
            (self.urls['add'], self.author_client, HTTPStatus.OK),
            (self.urls['success'], self.author_client, HTTPStatus.OK),
            (self.urls['detail'], self.author_client, HTTPStatus.OK),
            (self.urls['edit'], self.author_client, HTTPStatus.OK),
            (self.urls['delete'], self.author_client, HTTPStatus.OK),
            (self.urls['detail'], self.not_author_client,
             HTTPStatus.NOT_FOUND),
            (self.urls['edit'], self.not_author_client, HTTPStatus.NOT_FOUND),
            (self.urls['delete'], self.not_author_client,
             HTTPStatus.NOT_FOUND),
        )
        for url, client, expected_status in urls:
            with self.subTest(url=url):
                request_type = client.post if url == self.urls['logout'] else (
                    client.get
                )
                self.assertEqual(
                    request_type(url).status_code, expected_status)

    def test_redirect_for_anonymous_client(self):
        """
        Тестируем редирект анонимного пользователя на страницу для входа,
        если он пытается получить доступ к страницам для
        авторизованных пользователей.
        """
        urls = (
            self.urls['list'],
            self.urls['add'],
            self.urls['success'],
            self.urls['detail'],
            self.urls['edit'],
            self.urls['delete'],
        )
        for url in urls:
            with self.subTest(url=url):
                self.assertRedirects(
                    self.client.get(url),
                    f'{self.urls['login']}?next={url}'
                )
