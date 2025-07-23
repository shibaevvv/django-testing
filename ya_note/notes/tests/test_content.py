from notes.forms import NoteForm

from .base_test_class import TestBaseClass


class TestContent(TestBaseClass):

    def test_authorized_client_has_form(self):
        """
        Проверка наличия формы на страницах добавления и
        редактирования заметки.
        """
        for url in (self.urls['add'], self.urls['edit']):
            with self.subTest(url=url):
                response = self.author_client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(
                    response.context['form'],
                    NoteForm
                )

    def test_notes_list_for_different_users(self):
        """
        Проверка наличия отдельной заметки и отсутсвие чужих заметок
        в списке заметок автора.
        """
        author_notes = (
            self.author_client.get(self.urls['list']).context['object_list']
        )
        self.assertIn(self.note, author_notes)
        self.assertNotIn(self.not_author_note, author_notes)
