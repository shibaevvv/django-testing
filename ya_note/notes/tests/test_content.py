from notes.forms import NoteForm

from .base_test_class import TestBaseClass, LIST_URL, ADD_URL, EDIT_URL


class TestContent(TestBaseClass):

    def test_authorized_client_has_form(self):
        """
        Проверка наличия формы на страницах добавления и
        редактирования заметки.
        """
        for url in (ADD_URL, EDIT_URL):
            with self.subTest(url=url):
                response = self.author_client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(
                    response.context['form'],
                    NoteForm
                )

    def test_note_in_author_notes_list(self):
        """Проверка наличия отдельной заметки в списке заметок автора."""
        author_notes = (
            self.author_client.get(LIST_URL).context['object_list']
        )
        self.assertIn(self.note, author_notes)
        author_note = author_notes.get(id=self.note.id)
        self.assertEqual(self.note.title, author_note.title)
        self.assertEqual(self.note.text, author_note.text)
        self.assertEqual(self.note.slug, author_note.slug)
        self.assertEqual(self.note.author, author_note.author)

    def test_note_not_in_user_notes_list(self):
        """Проверка отсутствия заметки автора в чужом списке заметок."""
        self.assertNotIn(
            self.note,
            self.not_author_client.get(LIST_URL).context['object_list']
        )
