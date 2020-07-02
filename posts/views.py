from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment, Category
from django.core.paginator import Paginator
from django.conf import settings
from django.contrib import messages
from .forms import PostModelForm
from django.contrib.auth.decorators import login_required
# Create your views here.
User = settings.AUTH_USER_MODEL

# this function returns all published posts of all users (timeline)
def posts_list(request):
    all_posts = Post.objects.filter(published = True)

    paginator = Paginator(all_posts, 3)
    page = request.GET.get('page')
    all_posts = paginator.get_page(page)

    context = {
        'all_posts': all_posts
    }
    return render(request, 'postslist.html', context)

# this function used to get all posts of a particular user and logedin user
def user_posts(request, user):
    if request.user.username == user:
        if request.method == 'POST':
            all_posts = Post.objects.filter(user__username = user, category = request.POST['category'])
        else:
            all_posts = Post.objects.filter(user__username = user)
    else:
        all_posts = Post.objects.filter(published = True, user__username = user, category = request.POST['category'])


    paginator = Paginator(all_posts, 3)
    page = request.GET.get('page')
    all_posts = paginator.get_page(page)
    categories = Category.objects.all()
    context = {
        'all_posts': all_posts,
        'categories': categories
    }
    return render(request, 'user_posts.html', context)


@login_required(login_url='/accounts/signin')
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk, published=True)
    try:
        comment = Comment.objects.create(
        user=request.user, post = post, comment = request.GET['comment']
        )
        messages.success(request, "Comment Added!")
        return redirect('/posts/{}'.format(pk))
    except Exception as e:
        messages.error(e)
        return redirect('/posts/{}'.format(pk))

# display all comments received
@login_required(login_url='/accounts/signin')
def display_all_comments(request):
    comments = Comment.objects.filter(post__user=request.user)
    context = {
      'comments': comments
    }
    return render(request, 'all_posts_comments.html', context)


#CRUD
def post_detail(request, pk):
    post = get_object_or_404(Post, id=pk)
    comments = Comment.objects.filter(post__pk=pk)
    context = {
        'post': post,
        'comments': comments
    }
    if request.user == post.user:
        return render(request, 'post_details.html', context)
    else:
        post = get_object_or_404(Post, id=pk, published=True)

    return render(request, 'post_details.html', context)

@login_required(login_url='/accounts/signin')
def create_post(request):
    form = PostModelForm()
    if request.method == 'POST':
        form = PostModelForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            messages.success(request, "Post Created Successfully!!")
            return redirect('/posts/allposts')

    context = {
        'form': form
    }

    return render(request, 'create_post.html', context)

@login_required(login_url='/accounts/signin')
def update_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user == post.user:
        form = PostModelForm(request.POST or None, request.FILES or None, instance=post)
        if form.is_valid():
            form.save()
            return redirect('/posts/{}'.format(post.pk))

        context = {
            'form': form
        }

        return render(request, 'update_post.html', context)
    else:
        messages.error(request, "Access Denied!")
        return redirect('/posts/allposts')

@login_required(login_url='/accounts/signin/')
def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user == post.user:
        post.delete()
        return redirect('/posts/user_posts/{}'.format(request.user.username))
    else:
        messages.success(request, "Access Denied!")
        return redirect('/posts/allposts')
