from http import HTTPStatus

from django.core.exceptions import ObjectDoesNotExist
from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note

from .base_test_class import (
    TestBaseClass, URL_REDIRECT_ADD, URL_SUCCESS, URL_EDIT, URL_ADD, URL_DELETE
)


class TestLogic(TestBaseClass):

    def add_author_new_note(self):
        """Функция добавляет новую статью автора с проверками создания."""
        notes_id = (list(Note.objects.all().values_list('id', flat=True)))
        self.assertRedirects(
            self.author_client.post(URL_ADD, data=self.form_data),
            URL_SUCCESS
        )
        new_notes = Note.objects.exclude(id__in=notes_id)
        self.assertEqual(new_notes.count(), 1)
        return new_notes.get()

    def check_note_fields(self, note=None, title=None, text=None, slug=None):
        """
        Функция проверяет состояние полей заметки на равенство после
        попыток удалить или изменить ее.
        """
        title = title or self.note.title
        text = text or self.note.text
        slug = slug or self.note.slug
        note = note or Note.objects.get(id=self.note.id)
        self.assertEqual(note.title, title)
        self.assertEqual(note.text, text)
        self.assertEqual(note.slug, slug)
        self.assertEqual(note.author, self.author)

    def test_user_can_create_note(self):
        """Проверка возможности создать заметку залогиненому пользователю."""
        self.check_note_fields(
            note=self.add_author_new_note(),
            title=self.form_data['title'],
            text=self.form_data['text'],
            slug=self.form_data['slug']
        )

    def test_anonymous_user_cant_create_note(self):
        """Проверка, что анонимный пользователь не может создать заметку."""
        notes_obj_before = Note.objects.all()
        self.assertRedirects(
            self.client.post(URL_ADD, data=self.form_data),
            URL_REDIRECT_ADD
        )
        self.assertEqual(notes_obj_before.count(), Note.objects.count())
        self.assertQuerySetEqual(notes_obj_before, Note.objects.all())

    def test_empty_slug(self):
        """
        Проверяем автоматическое формирование slug при создании
        заметки, если поле не заполнено.
        """
        self.form_data.pop('slug')
        self.check_note_fields(
            note=self.add_author_new_note(),
            title=self.form_data['title'],
            text=self.form_data['text'],
            slug=slugify(self.form_data['title'])
        )

    def test_not_unique_slug(self):
        """Проверка невозможности создать две заметки с одинаковым slug."""
        notes_obj_before = Note.objects.all()
        self.form_data['slug'] = self.note.slug
        self.assertFormError(
            self.author_client.post(
                URL_ADD, data=self.form_data).context['form'],
            'slug',
            errors=(self.note.slug + WARNING)
        )
        self.assertQuerySetEqual(notes_obj_before, Note.objects.all())

    def test_author_can_edit_note(self):
        """Проверка, что автор может редактировать свои заметки."""
        self.assertRedirects(
            self.author_client.post(URL_EDIT, self.form_data),
            URL_SUCCESS
        )
        self.check_note_fields(
            title=self.form_data['title'],
            text=self.form_data['text'],
            slug=self.form_data['slug']
        )

    def test_not_author_cant_edit_note(self):
        """Проверка, что заметку не может редактировать не автор."""
        self.assertEqual(
            self.not_author_client.post(
                URL_EDIT, self.form_data).status_code,
            HTTPStatus.NOT_FOUND
        )
        self.check_note_fields()

    def test_author_can_delete_note(self):
        """Проверка, что автор может удалить свою заметку."""
        notes_count_before = Note.objects.count()
        self.assertRedirects(
            self.author_client.post(URL_DELETE),
            URL_SUCCESS
        )
        self.assertEqual(Note.objects.count(), notes_count_before - 1)
        with self.assertRaises(ObjectDoesNotExist):
            Note.objects.get(id=self.note.id)

    def test_not_author_cant_delete_note(self):
        """Проверка, что не автор не может удалить чужую заметку."""
        notes_obj_before = Note.objects.all()
        self.assertEqual(
            self.not_author_client.post(URL_DELETE).status_code,
            HTTPStatus.NOT_FOUND
        )
        self.assertEqual(notes_obj_before.count(), Note.objects.count())
        self.assertQuerySetEqual(notes_obj_before, Note.objects.all())
        self.check_note_fields()
