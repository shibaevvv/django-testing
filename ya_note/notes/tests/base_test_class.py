from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

from notes.models import Note

User = get_user_model()

NOTE_SLUG = 'note_slug'

URL_HOME = reverse('notes:home')
URL_LOGIN = reverse('users:login')
URL_LOGOUT = reverse('users:logout')
URL_SIGNUP = reverse('users:signup')
URL_LIST = reverse('notes:list')
URL_ADD = reverse('notes:add')
URL_SUCCESS = reverse('notes:success')
URL_DETAIL = reverse('notes:detail', args=(NOTE_SLUG,))
URL_EDIT = reverse('notes:edit', args=(NOTE_SLUG,))
URL_DELETE = reverse('notes:delete', args=(NOTE_SLUG,))
URL_REDIRECT_LIST = f'{URL_LOGIN}?next={URL_LIST}'
URL_REDIRECT_ADD = f'{URL_LOGIN}?next={URL_ADD}'
URL_REDIRECT_SUCCESS = f'{URL_LOGIN}?next={URL_SUCCESS}'
URL_REDIRECT_DETAIL = f'{URL_LOGIN}?next={URL_DETAIL}'
URL_REDIRECT_EDIT = f'{URL_LOGIN}?next={URL_EDIT}'
URL_REDIRECT_DELETE = f'{URL_LOGIN}?next={URL_DELETE}'


class TestBaseClass(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Пользователи
        cls.author = User.objects.create(username='Автор')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.not_author = User.objects.create(username='Не автор')
        cls.not_author_client = Client()
        cls.not_author_client.force_login(cls.not_author)
        # Заметки
        cls.note = Note.objects.create(
            title='Заголовок', text='Текст',
            slug=NOTE_SLUG, author=cls.author)

        cls.form_data = {'title': 'Новый заголовок',
                         'text': 'Новый текст заметки',
                         'slug': 'novyij-zagolovok'}
