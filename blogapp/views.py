from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView

from .models import Post


class PostListView(ListView):
    """Альтернативное представление списка постов"""

    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = "blogapp/post/list.html"


def post_list(request):
    postlist = Post.published.all()
    # Постраничная разбивка с 3 постами на страницу
    paginator = Paginator(postlist, 3)
    page_number = request.GET.get("page", 1)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        # Если page_number находится вне диапазона, то выдать последнюю страницу
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)
    return render(request, "blogapp/post/list.html", {"posts": posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post, status=Post.Status.PUBLISHED, slug=post, publish__year=year, publish__month=month, publish__day=day
    )
    return render(request, "blogapp/post/detail.html", {"post": post})
