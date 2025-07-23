from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

from notes.models import Note

User = get_user_model()


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
            slug='slug_1', author=cls.author)
        cls.not_author_note = Note.objects.create(
            title='Заголовок не автора', text='Текст не автора',
            slug='slug_2', author=cls.not_author)
        cls.notes_count = Note.objects.count()
        # УРЛы
        cls.urls = {
            'home': reverse('notes:home'),
            'login': reverse('users:login'),
            'logout': reverse('users:logout'),
            'signup': reverse('users:signup'),
            'list': reverse('notes:list'),
            'add': reverse('notes:add'),
            'success': reverse('notes:success'),
            'detail': reverse('notes:detail', args=(cls.note.slug,)),
            'edit': reverse('notes:edit', args=(cls.note.slug,)),
            'delete': reverse('notes:delete', args=(cls.note.slug,)),
        }
        cls.form_data = {'title': 'Новый заголовок',
                         'text': 'Новый текст заметки',
                         'slug': 'novyij-zagolovok'}

    def add_note(self, anonymous=False):
        sender = self.client if anonymous else self.author_client
        return sender.post(
            self.urls['add'],
            data=self.form_data
        )
