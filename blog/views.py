from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm
from django.core.mail import send_mail
from .models import Post, Comment
from .forms import EmailPostForm, CommentForm
from taggit.models import Tag
from django.db.models import Count

# Create your views here.




def index(request):
    return render(request, 'index.html')   

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month, publish__day=day)
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    new_comment = None
    comment_form = CommentForm(data=request.POST)
    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
        else:
            comment_form = CommentForm()
    post_tags_ids = post.tags.values_list('id', flat=True) 
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('same_tags','publish')[:4]
    return render(request, 'blog/detail.html', {'post': post, 'comments': comments, 'new_comment': new_comment, 'comment_form': comment_form, 'similar_posts': similar_posts})

def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    posts = Post.published.order_by()
    object_list = Post.published.order_by()
    paginator = Paginator(object_list, 2) # 2 posts in each page
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        page_obj = paginator.get_page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        page_obj= paginator.get_page(paginator.num_pages)
    return render(request, 'blog/post_list.html', {'page_obj': page_obj, 'posts': posts, 'tag': tag})
    

class PostListView(ListView):
    queryset = Post.published.order_by()
    context_object_name = 'posts'
    paginate_by = 2
    template_name = 'blog/post_list.html'



def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
    # Form was submitted
        form = EmailPostForm(request.POST)
    
        if form.is_valid():
        # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'danielidhosa98@gmail.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()

    return render(request, 'blog/share.html', {'post': post, 'form': form, 'sent': sent})