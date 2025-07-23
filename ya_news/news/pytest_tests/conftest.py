from datetime import datetime, timedelta

import pytest
from django.conf import settings
from django.test.client import Client
from django.urls import reverse

from news.models import Comment, News


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def news(author):
    return News.objects.create(title='Новость', text='Текст новости',)


@pytest.fixture
def news_id(news):
    return (news.pk,)


@pytest.fixture
def news_collection(author):
    return News.objects.bulk_create(
        News(
            title=f'Новость {index}',
            text='Текст новости.',
            date=datetime.today() - timedelta(days=index)
        ) for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    )


@pytest.fixture
def comment(author, news):
    return Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария'
    )


@pytest.fixture
def comment_id(comment):
    return (comment.pk,)


@pytest.fixture
def comment_collection(author, news):
    return Comment.objects.bulk_create(
        Comment(
            news=news,
            author=author,
            text=f'Текст {index}',
            created=datetime.today() - timedelta(days=index)
        ) for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    )


@pytest.fixture
def form_data():
    return {
        'text': 'Отредактированный комментарий'
    }


@pytest.fixture
def url_home():
    return reverse('news:home')


@pytest.fixture
def url_news_detail(news_id):
    return reverse('news:detail', args=news_id)


@pytest.fixture
def url_login():
    return reverse('users:login')


@pytest.fixture
def url_logout():
    return reverse('users:logout')


@pytest.fixture
def url_signup():
    return reverse('users:signup')


@pytest.fixture
def url_delete_comment(comment_id):
    return reverse('news:delete', args=comment_id)


@pytest.fixture
def url_edit_comment(comment_id):
    return reverse('news:edit', args=comment_id)
