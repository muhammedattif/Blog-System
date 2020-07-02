from django.urls import path

from . import views

app_name = 'posts'
urlpatterns = [
    path('allposts', views.posts_list, name='all_posts'),
    path('allcomments/', views.display_all_comments, name='allcomments'),
    path('create_post/', views.create_post, name='create_post'),
    path('user_posts/<user>', views.user_posts, name='user_posts'),
    path('addcomment/<pk>', views.add_comment, name='add_comment'),
    path('<slug>/update/', views.update_post, name='update'),
    path('<slug>/delete/', views.delete_post, name='delete'),
    path('<pk>', views.post_detail, name='posts'),



]
