from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

from notes.models import Note

User = get_user_model()

NOTE_SLUG = 'note_slug'

HOME_URL = reverse('notes:home')
LOGIN_URL = reverse('users:login')
LOGOUT_URL = reverse('users:logout')
SIGNUP_URL = reverse('users:signup')
LIST_URL = reverse('notes:list')
ADD_URL = reverse('notes:add')
SUCCESS_URL = reverse('notes:success')
DETAIL_URL = reverse('notes:detail', args=(NOTE_SLUG,))
EDIT_URL = reverse('notes:edit', args=(NOTE_SLUG,))
DELETE_URL = reverse('notes:delete', args=(NOTE_SLUG,))
REDIRECT_TO_LIST_URL = f'{LOGIN_URL}?next={LIST_URL}'
REDIRECT_TO_ADD_URL = f'{LOGIN_URL}?next={ADD_URL}'
REDIRECT_TO_SUCCESS_URL = f'{LOGIN_URL}?next={SUCCESS_URL}'
REDIRECT_TO_DETAIL_URL = f'{LOGIN_URL}?next={DETAIL_URL}'
REDIRECT_TO_EDIT_URL = f'{LOGIN_URL}?next={EDIT_URL}'
REDIRECT_TO_DELETE_URL = f'{LOGIN_URL}?next={DELETE_URL}'


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
