from http import HTTPStatus

from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment


def test_user_can_create_comment(author_client, author, form_data,
                                 url_news_detail):
    """Тест, что авторизованный пользователь может отправить комментарий."""
    assertRedirects(
        author_client.post(url_news_detail, data=form_data),
        url_news_detail + '#comments'
    )
    assert Comment.objects.count() == 1
    new_comment = Comment.objects.get()
    assert new_comment.text == form_data['text']
    assert new_comment.author == author


def test_anonymous_user_cant_create_comment(client, form_data, url_news_detail,
                                            url_login):
    """Тест, что анонимный пользователь не может отправить комментарий."""
    assertRedirects(
        client.post(url_news_detail, data=form_data),
        f'{url_login}?next={url_news_detail}'
    )
    assert Comment.objects.count() == 0, (
        'Убедитесь' + test_anonymous_user_cant_create_comment.__doc__[4:]
    )


def test_user_cant_use_bad_words_in_comment(author_client, form_data,
                                            url_news_detail):
    """Тест, что добавляемый комментарий не содержит запрещенные слова."""
    form_data['text'] = BAD_WORDS[0]
    assertFormError(
        author_client.post(url_news_detail, data=form_data).context['form'],
        'text',
        errors=(WARNING)
    )
    assert Comment.objects.count() == 0


def test_author_can_edit_comment(author_client, form_data, comment,
                                 url_edit_comment, url_news_detail):
    """Тест, что автор может редактировать свой комментарий."""
    assertRedirects(
        author_client.post(url_edit_comment, form_data),
        url_news_detail + '#comments'
    )
    comment.refresh_from_db()
    assert comment.text == form_data['text']


def test_author_can_delete_comment(author_client, url_delete_comment,
                                   url_news_detail):
    """Тест, что автор может удалить свой комментарий."""
    assertRedirects(
        author_client.post(url_delete_comment),
        url_news_detail + '#comments')
    assert Comment.objects.count() == 0


def test_other_user_cant_edit_comment(not_author_client, form_data, comment,
                                      url_edit_comment):
    """
    Тест, что авторизованный пользователь не может редактировать
    чужие комментарии.
    """
    assert not_author_client.post(url_edit_comment, form_data).status_code == (
        HTTPStatus.NOT_FOUND
    )
    comment_from_db = Comment.objects.get(id=comment.pk)
    assert comment.text == comment_from_db.text


def test_other_user_cant_delete_comment(not_author_client, url_delete_comment):
    """
    Тест, что авторизованный пользователь не может удалять чужие
    комментарии.
    """
    assert not_author_client.post(url_delete_comment).status_code == (
        HTTPStatus.NOT_FOUND
    )
    assert Comment.objects.count() == 1
