from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.core.mail import send_mail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from taggit.models import Tag

from blogapp.forms import CommentForm, EmailPostForm, SearchForm
from blogapp.models import Post


def post_share(request, post_id):
    # Извлечь пост по идендификатору id
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)

    sent = False

    if request.method == "POST":
        # То есть мы передаем форму на обработку
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # ПОля формы успешно прошли валидацию
            cd = form.cleaned_data
            posr_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {posr_url}\n\n" f"{cd['name']}'s comments: {cd['comments']}"
            send_mail(subject, message, "rushput@gmail.com", [cd["to"]])
            sent = True
    else:
        form = EmailPostForm()

    return render(request, "blogapp/post/share.html", {"post": post, "form": form, "sent": sent})


class PostListView(ListView):
    """Альтернативное представление списка постов"""

    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = "blogapp/post/list.html"


def post_list(request, tag_slug=None):
    postlist = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        postlist = postlist.filter(tags__in=[tag])
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
    return render(request, "blogapp/post/list.html", {"posts": posts, "tag": tag})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post, status=Post.Status.PUBLISHED, slug=post, publish__year=year, publish__month=month, publish__day=day
    )
    comments = post.comments.filter(active=True)
    form = CommentForm()
    # Список схожих постов
    post_tags_ids = post.tags.values_list("id", flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count("tags")).order_by("-same_tags", "-publish")[:4]

    return render(
        request,
        "blogapp/post/detail.html",
        {"post": post, "comments": comments, "form": form, "similar_posts": similar_posts},
    )


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)

    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        #  Создать объект класса Comment, не сохраняя его в БД
        comment = form.save(commit=False)
        # Назначить пост к комментарию
        comment.post = post
        # Сохранить комментарий в бд
        comment.save()

    return render(request, "blogapp/post/comment.html", {"post": post, "form": form, "comment": comment})


def post_search(request):
    form = SearchForm()
    query = None
    results = []

    if "query" in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data["query"]
            search_vector = SearchVector("title", weight="A") + SearchVector("body", weight="B")
            search_query = SearchQuery(query)
            results = (
                Post.published.annotate(search=search_vector, rank=SearchRank(search_vector, search_query))
                .filter(rank__gte=0.3)
                .order_by("-rank")
            )

    return render(request, "blogapp/post/search.html", {"form": form, "query": query, "results": results})
