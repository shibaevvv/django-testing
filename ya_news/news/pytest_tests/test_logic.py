from http import HTTPStatus

import pytest
from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

FORM_DATA = {'text': 'Новый комментарий'}
BAD_WORDS_FORM_DATA = [{'text': word} for word in BAD_WORDS]


def test_user_can_create_comment(author_client, news, author, news_detail_url,
                                 redirect_to_news_comments_url):
    """Тест, что авторизованный пользователь может отправить комментарий."""
    assertRedirects(
        author_client.post(news_detail_url, data=FORM_DATA),
        redirect_to_news_comments_url
    )
    assert Comment.objects.count() == 1
    new_comment = Comment.objects.get()
    assert new_comment.news == news
    assert new_comment.author == author
    assert new_comment.text == FORM_DATA['text']


def test_anonymous_user_cant_create_comment(client, news_detail_url,
                                            redirect_to_news_detail_url):
    """Тест, что анонимный пользователь не может отправить комментарий."""
    assertRedirects(
        client.post(news_detail_url, data=FORM_DATA),
        redirect_to_news_detail_url
    )
    assert Comment.objects.count() == 0


def test_author_can_edit_comment(author_client, comment,
                                 edit_comment_url,
                                 redirect_to_news_comments_url):
    """Тест, что автор может редактировать свой комментарий."""
    assertRedirects(
        author_client.post(edit_comment_url, data=FORM_DATA),
        redirect_to_news_comments_url
    )
    comment_from_db = Comment.objects.get(id=comment.pk)
    assert comment_from_db.news == comment.news
    assert comment_from_db.author == comment.author
    assert comment_from_db.text == FORM_DATA['text']


@pytest.mark.parametrize('bad_words_form_data', BAD_WORDS_FORM_DATA)
def test_user_cant_use_bad_words_in_comment(author_client, news_detail_url,
                                            bad_words_form_data):
    """Тест, что добавляемый комментарий не содержит запрещенные слова."""
    assertFormError(
        author_client.post(
            news_detail_url, data=bad_words_form_data).context['form'],
        'text',
        errors=(WARNING)
    )
    assert Comment.objects.count() == 0


def test_author_can_delete_comment(author_client, delete_comment_url,
                                   redirect_to_news_comments_url):
    """Тест, что автор может удалить свой комментарий."""
    assertRedirects(
        author_client.post(delete_comment_url),
        redirect_to_news_comments_url)
    assert Comment.objects.count() == 0


def test_other_user_cant_edit_comment(not_author_client, comment, news, author,
                                      edit_comment_url):
    """
    Тест, что авторизованный пользователь не может редактировать
    чужие комментарии.
    """
    assert not_author_client.post(
        edit_comment_url,
        FORM_DATA).status_code == HTTPStatus.NOT_FOUND
    comment_from_db = Comment.objects.get(id=comment.pk)
    assert comment.news == comment_from_db.news
    assert comment.author == comment_from_db.author
    assert comment.text == comment_from_db.text


def test_other_user_cant_delete_comment(not_author_client, delete_comment_url,
                                        comment):
    """
    Тест, что авторизованный пользователь не может удалять чужие
    комментарии.
    """
    assert not_author_client.post(delete_comment_url).status_code == (
        HTTPStatus.NOT_FOUND
    )
    assert Comment.objects.count() == 1
    comment_from_db = Comment.objects.get(id=comment.pk)
    assert comment.news == comment_from_db.news
    assert comment.author == comment_from_db.author
    assert comment.text == comment_from_db.text
