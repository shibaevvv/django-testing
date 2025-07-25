from datetime import datetime, timedelta

import pytest
from django.conf import settings
from django.test.client import Client
from django.urls import reverse
from django.utils import timezone

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
def news_collection(author):
    News.objects.bulk_create(
        News(
            title=f'Новость {index}',
            text='Текст новости.',
            date=datetime.now() - timedelta(days=index)
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
def comment_collection(author, news):
    for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1):
        comment = Comment.objects.create(
            news=news, author=author, text=f'Текст {index}')
        comment.created = timezone.now() - timedelta(days=index)
        comment.save()


@pytest.fixture
def home_url():
    return reverse('news:home')


@pytest.fixture
def news_detail_url(news):
    return reverse('news:detail', args=(news.pk,))


@pytest.fixture
def login_url():
    return reverse('users:login')


@pytest.fixture
def logout_url():
    return reverse('users:logout')


@pytest.fixture
def signup_url():
    return reverse('users:signup')


@pytest.fixture
def delete_comment_url(comment):
    return reverse('news:delete', args=(comment.pk,))


@pytest.fixture
def edit_comment_url(comment):
    return reverse('news:edit', args=(comment.pk,))


@pytest.fixture
def redirect_to_news_comments_url(news_detail_url):
    return f'{news_detail_url}#comments'


@pytest.fixture
def redirect_to_comment_edit_url(login_url, edit_comment_url):
    return f'{login_url}?next={edit_comment_url}'


@pytest.fixture
def redirect_to_comment_delete_url(login_url, delete_comment_url):
    return f'{login_url}?next={delete_comment_url}'


@pytest.fixture
def redirect_to_news_detail_url(login_url, news_detail_url):
    return f'{login_url}?next={news_detail_url}'
