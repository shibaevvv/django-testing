from http import HTTPStatus

from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note

from .base_test_class import TestBaseClass


class TestLogic(TestBaseClass):

    def test_user_can_create_note(self):
        """Проверка возможности создать заметку залогиненому пользователю."""
        self.assertRedirects(self.add_note(), self.urls['success'])
        self.assertEqual(Note.objects.count(), self.notes_count + 1)
        new_note = Note.objects.get(slug=self.form_data['slug'])
        self.assertEqual(new_note.title, self.form_data['title'])
        self.assertEqual(new_note.text, self.form_data['text'])
        self.assertEqual(new_note.slug, self.form_data['slug'])
        self.assertEqual(new_note.author, self.author)

    def test_anonymous_user_cant_create_note(self):
        """Проверка, что анонимный пользователь не может создать заметку."""
        self.assertRedirects(
            self.add_note(anonymous=True),
            f'{self.urls['login']}?next={self.urls['add']}'
        )
        self.assertEqual(Note.objects.count(), self.notes_count)

    def test_not_unique_slug(self):
        """Проверка невозможности создать две заметки с одинаковым slug."""
        self.form_data['slug'] = self.note.slug
        self.assertFormError(
            self.add_note().context['form'],
            'slug',
            errors=(self.note.slug + WARNING)
        )
        self.assertEqual(Note.objects.count(), self.notes_count)

    def test_empty_slug(self):
        """
        Проверяем автоматическое формирование slug при создании
        заметки, если поле не заполнено.
        """
        self.form_data.pop('slug')
        self.assertRedirects(self.add_note(), self.urls['success'])
        self.assertEqual(Note.objects.count(), self.notes_count + 1)
        new_note = Note.objects.get(id=self.notes_count + 1)
        expected_slug = slugify(self.form_data['title'])
        self.assertEqual(new_note.slug, expected_slug)

    def test_author_can_edit_note(self):
        """Проверка, что автор может редактировать свои заметки."""
        self.assertRedirects(
            self.author_client.post(self.urls['edit'], self.form_data),
            self.urls['success']
        )
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, self.form_data['title'])
        self.assertEqual(self.note.text, self.form_data['text'])
        self.assertEqual(self.note.slug, self.form_data['slug'])

    def test_not_author_cant_edit_note(self):
        """Проверка, что заметку не может редактировать не автор."""
        self.assertEqual(
            self.not_author_client.post(
                self.urls['edit'], self.form_data).status_code,
            HTTPStatus.NOT_FOUND
        )
        note_from_db = Note.objects.get(slug=self.note.slug)
        self.assertEqual(self.note.title, note_from_db.title)
        self.assertEqual(self.note.text, note_from_db.text)
        self.assertEqual(self.note.slug, note_from_db.slug)

    def test_author_can_delete_note(self):
        """Проверка, что автор может удалить свою заметку."""
        self.assertRedirects(
            self.author_client.post(self.urls['delete']),
            self.urls['success']
        )
        self.assertEqual(Note.objects.count(), self.notes_count - 1)

    def test_not_author_cant_delete_note(self):
        """Проверка, что не автор не может удалить чужую заметку."""
        self.assertEqual(
            self.not_author_client.post(self.urls['delete']).status_code,
            HTTPStatus.NOT_FOUND
        )
        self.assertEqual(Note.objects.count(), self.notes_count)
