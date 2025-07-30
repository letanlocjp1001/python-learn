from django.core.paginator import Paginator # Tạo phân trang
from django.shortcuts import render, get_object_or_404 # Lấy đối tượng hoặc trả về 404
from .models import Post # Nhập mô hình Post
from django.db.models import Q # Dùng để lọc bài viết


def index(request):
    query = request.GET.get('q', '') # Lấy từ khóa tìm kiếm từ URL (?q=keyword)
    post_list = Post.objects.all().order_by('-created_at')

    if query:
        post_list = post_list.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )

    # Sử dụng Paginator để phân trang
    paginator = Paginator(post_list, 5)  # Show 5 posts per page
    page_number = request.GET.get('page') # Lấy số trang từ URL (?page=2)

    posts = paginator.get_page(page_number)
    return render(request, 'blog/index.html', {
        'posts': posts,
        'query': query  # Truyền từ khóa tìm kiếm vào template
        })

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    # 🔹 Lấy bài viết trước (bài cũ hơn, created_at < bài hiện tại, gần nhất)
    prev_post = Post.objects.filter(created_at__lt=post.created_at).order_by('-created_at').first()

    # 🔹 Lấy bài viết sau (bài mới hơn, created_at > bài hiện tại, gần nhất)
    next_post = Post.objects.filter(created_at__gt=post.created_at).order_by('created_at').first()

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'prev_post' : prev_post,
        'next_post' : next_post,

        })


