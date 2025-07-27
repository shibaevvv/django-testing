from http import HTTPStatus

from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note

from .base_test_class import (
    TestBaseClass, REDIRECT_TO_ADD_URL, SUCCESS_URL, EDIT_URL, ADD_URL,
    DELETE_URL
)


class TestLogic(TestBaseClass):

    def add_author_new_note(self, slug):
        """Функция добавляет новую статью автора с проверками создания."""
        notes_id = (list(Note.objects.all().values_list('id', flat=True)))
        self.assertRedirects(
            self.author_client.post(ADD_URL, data=self.form_data),
            SUCCESS_URL
        )
        new_notes = Note.objects.exclude(id__in=notes_id)
        self.assertEqual(new_notes.count(), 1)
        new_note = new_notes.get()
        self.assertEqual(new_note.title, self.form_data['title'])
        self.assertEqual(new_note.text, self.form_data['text'])
        self.assertEqual(new_note.slug, slug)
        self.assertEqual(new_note.author, self.author)

    def test_user_can_create_note(self):
        """Проверка возможности создать заметку залогиненому пользователю."""
        self.add_author_new_note(self.form_data['slug'])

    def test_anonymous_user_cant_create_note(self):
        """Проверка, что анонимный пользователь не может создать заметку."""
        notes = set(Note.objects.all())
        self.assertRedirects(
            self.client.post(ADD_URL, data=self.form_data),
            REDIRECT_TO_ADD_URL
        )
        self.assertEqual(notes, set(Note.objects.all()))

    def test_empty_slug(self):
        """
        Проверяем автоматическое формирование slug при создании
        заметки, если поле не заполнено.
        """
        self.form_data.pop('slug')
        self.add_author_new_note(slugify(self.form_data['title']))

    def test_not_unique_slug(self):
        """Проверка невозможности создать две заметки с одинаковым slug."""
        self.form_data['slug'] = self.note.slug
        notes = set(Note.objects.all())
        self.assertFormError(
            self.author_client.post(
                ADD_URL, data=self.form_data).context['form'],
            'slug',
            errors=(self.note.slug + WARNING)
        )
        self.assertEqual(notes, set(Note.objects.all()))

    def test_author_can_edit_note(self):
        """Проверка, что автор может редактировать свои заметки."""
        self.assertRedirects(
            self.author_client.post(EDIT_URL, self.form_data),
            SUCCESS_URL
        )
        note = Note.objects.get(id=self.note.id)
        self.assertEqual(note.title, self.form_data['title'])
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.slug, self.form_data['slug'])
        self.assertEqual(note.author, self.note.author)

    def test_not_author_cant_edit_note(self):
        """Проверка, что заметку не может редактировать не автор."""
        self.assertEqual(
            self.not_author_client.post(
                EDIT_URL, self.form_data).status_code,
            HTTPStatus.NOT_FOUND
        )
        note = Note.objects.get(id=self.note.id)
        self.assertEqual(note.title, self.note.title)
        self.assertEqual(note.text, self.note.text)
        self.assertEqual(note.slug, self.note.slug)
        self.assertEqual(note.author, self.note.author)

    def test_author_can_delete_note(self):
        """Проверка, что автор может удалить свою заметку."""
        notes_count_before = Note.objects.count()
        self.assertRedirects(
            self.author_client.post(DELETE_URL),
            SUCCESS_URL
        )
        self.assertEqual(Note.objects.count(), notes_count_before - 1)
        self.assertFalse(Note.objects.filter(id=self.note.id).exists())

    def test_not_author_cant_delete_note(self):
        """Проверка, что не автор не может удалить чужую заметку."""
        notes = set(Note.objects.all())
        self.assertEqual(
            self.not_author_client.post(DELETE_URL).status_code,
            HTTPStatus.NOT_FOUND
        )
        self.assertEqual(notes, set(Note.objects.all()))
        note = Note.objects.get(id=self.note.id)
        self.assertEqual(note.title, self.note.title)
        self.assertEqual(note.text, self.note.text)
        self.assertEqual(note.slug, self.note.slug)
        self.assertEqual(note.author, self.author)
