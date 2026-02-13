from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse, Http404
from django.views.decorators.http import require_http_methods
from services.article_service import ArticleService
from articles.models import Article, Category, Tag


def home(request):
    """Головна сторінка з різними блоками контенту"""
    featured_articles = ArticleService.get_featured_articles(limit=1)
    latest_news = ArticleService.get_latest_articles(limit=6)
    popular_articles = ArticleService.get_popular_articles(limit=6, days=30)
    
    # Отримати статті за категоріями
    interviews = ArticleService.get_latest_articles(limit=4, category_slug='interviews')
    reviews = ArticleService.get_latest_articles(limit=4, category_slug='reviews')
    
    context = {
        'featured_article': featured_articles[0] if featured_articles else None,
        'latest_news': latest_news,
        'popular_articles': popular_articles,
        'interviews': interviews,
        'reviews': reviews,
    }
    return render(request, 'articles/home.html', context)


def article_list(request):
    """Список всіх статей з пагінацією"""
    articles = Article.objects.filter(
        status='published'
    ).select_related('author', 'category').prefetch_related('tags')
    
    paginator = Paginator(articles, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'articles/article_list.html', context)


def article_detail(request, slug):
    """Детальна сторінка статті"""
    article = ArticleService.get_article_by_slug(slug)
    
    if not article:
        raise Http404("Статтю не знайдено")
    
    # Збільшити кількість переглядів
    ArticleService.increment_views(article)
    
    # Отримати схожі статті
    related_articles = ArticleService.get_related_articles(article, limit=4)
    
    context = {
        'article': article,
        'related_articles': related_articles,
    }
    return render(request, 'articles/article_detail.html', context)


def category_detail(request, slug):
    """Сторінка категорії зі статтями"""
    page_number = request.GET.get('page', 1)
    page_obj, category = ArticleService.get_articles_by_category(slug, page=page_number)
    
    if not category:
        raise Http404("Категорію не знайдено")
    
    context = {
        'category': category,
        'page_obj': page_obj,
    }
    return render(request, 'articles/category_detail.html', context)


def tag_detail(request, slug):
    """Сторінка тегу зі статтями"""
    page_number = request.GET.get('page', 1)
    page_obj, tag = ArticleService.get_articles_by_tag(slug, page=page_number)
    
    if not tag:
        raise Http404("Тег не знайдено")
    
    context = {
        'tag': tag,
        'page_obj': page_obj,
    }
    return render(request, 'articles/tag_detail.html', context)


def author_detail(request, username):
    """Сторінка автора зі статтями"""
    page_number = request.GET.get('page', 1)
    page_obj, author = ArticleService.get_articles_by_author(username, page=page_number)
    
    if not author:
        raise Http404("Автора не знайдено")
    
    context = {
        'author': author,
        'page_obj': page_obj,
    }
    return render(request, 'articles/author_detail.html', context)


def search(request):
    """Пошук статей"""
    query = request.GET.get('q', '').strip()
    page_number = request.GET.get('page', 1)
    
    if query:
        page_obj = ArticleService.search_articles(query, page=page_number)
    else:
        page_obj = None
    
    context = {
        'query': query,
        'page_obj': page_obj,
    }
    return render(request, 'articles/search.html', context)


@require_http_methods(["GET"])
def live_search(request):
    """AJAX пошук для live search"""
    query = request.GET.get('q', '').strip()
    
    if len(query) < 2:
        return JsonResponse({'results': []})
    
    articles = Article.objects.filter(
        Q(title__icontains=query) | Q(short_description__icontains=query),
        status='published'
    ).select_related('author', 'category')[:5]
    
    results = [{
        'title': article.title,
        'url': article.get_absolute_url(),
        'short_description': article.short_description[:100] + '...' if len(article.short_description) > 100 else article.short_description,
        'category': article.category.name if article.category else '',
    } for article in articles]
    
    return JsonResponse({'results': results})


def handler404(request, exception):
    """Кастомна сторінка 404"""
    return render(request, 'articles/404.html', status=404)


def handler500(request):
    """Кастомна сторінка 500 - простий HTML без залежностей"""
    try:
        from django.template import loader
        from django.http import HttpResponseServerError
        # Використовуємо простий шаблон без extends та context_processors
        template = loader.get_template('articles/500.html')
        return HttpResponseServerError(template.render({}, request))
    except Exception:
        # Якщо навіть рендеринг помилки не працює, повертаємо простий HTML
        from django.http import HttpResponseServerError
        html = """<!DOCTYPE html><html><head><meta charset="utf-8"><title>500</title></head><body><h1>500</h1><p>Помилка сервера</p><a href="/">На головну</a></body></html>"""
        return HttpResponseServerError(html, content_type='text/html; charset=utf-8')
