# test_content.py
import pytest
from django.conf import settings

from news.forms import CommentForm


@pytest.mark.usefixtures('news_collection')
def test_news_ammount_on_home_page(client, url_home):
    """Проверка, что количество новостей на главной странице не более 10."""
    assert (client.get(url_home).context['object_list'].count()
            <= settings.NEWS_COUNT_ON_HOME_PAGE)


@pytest.mark.usefixtures('news_collection')
def test_news_order_in_home_page(client, url_home):
    """Проверка сортировки новостей. Свежие новости в начале списка."""
    all_dates = [news.date for news in (
        client.get(url_home).context['object_list']
    )]
    assert all_dates == sorted(all_dates, reverse=True)


@pytest.mark.usefixtures('comment_collection')
def test_comments_order(client, url_news_detail):
    """
    Проверка сортировки комментариев на странице отдельной новости.
    Старые комментарии в начале списка, а новые - в конце.
    """
    all_dates = [comment.created for comment in (
        client.get(url_news_detail).context['news'].comment_set.all()
    )
    ]
    assert all_dates == sorted(all_dates)


def test_detail_page_for_user_contains_form(author_client, url_news_detail):
    """
    Проверка, что форма отправки комментария к новости доступна
    авторизованному пользователю.
    """
    response = author_client.get(url_news_detail)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)


def test_detail_page_for_anonimus_not_contains_form(client, url_news_detail):
    """
    Проверка, что форма отправки комментария к новости не доступна
    анонимному пользователю.
    """
    response = client.get(url_news_detail)
    assert 'form' not in response.context
