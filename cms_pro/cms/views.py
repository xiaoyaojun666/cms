from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404

from .doc_parse.parse_service import summarize_paper
from .models import Category, Item, Paper
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.core.paginator import Paginator


def item_summary(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    # 根据item.paper_url去查询Paper表中的pdf字段
    # 模拟处理 - 你可以在这里加上具体的处理逻辑
    paper = get_object_or_404(Paper, paper_url=item.paper_url)
    pdf_path = paper.pdf_path
    summary = summarize_paper(pdf_path)
    # 将markdown内容返回为JSON
    return JsonResponse({'markdown_content': summary})


# 主页面展示
def index(request):
    categories = Category.objects.all()
    return render(request, 'cms/index.html', {'categories': categories})


# 按类别返回项目
# 按类别返回项目
def category_items(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    items = Item.objects.filter(category=category).order_by('published_date')  # 确保进行排序
    paginator = Paginator(items, 10)  # 每页显示10个item
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # 渲染items列表为HTML
    items_html = render_to_string('cms/items_list.html', {'page_obj': page_obj, 'category': category})

    return JsonResponse({
        'category_name': category.name,
        'items_html': items_html,
        'pagination_html': render_to_string('cms/pagination.html', {'page_obj': page_obj, 'category': category})
    })


def item_detail(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    return render(request, 'cms/item_detail.html', {'item': item})


def category_detail(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    items = Item.objects.filter(category=category)
    return render(request, 'cms/category_detail.html', {'category': category, 'items': items})


def search(request):
    query = request.GET.get('query')
    search_type = request.GET.get('type')
    if search_type == 'title':
        items = Item.objects.filter(title__icontains=query)
    elif search_type == 'date':
        items = Item.objects.filter(published_date__date=query)
    elif search_type == 'category':
        category = get_object_or_404(Category, name__icontains=query)
        items = Item.objects.filter(category=category)
    else:
        items = Item.objects.all()
    return render(request, 'cms/search_results.html', {'items': items})
