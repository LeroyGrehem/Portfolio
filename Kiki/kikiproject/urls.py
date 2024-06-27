from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('profile/<int:pk>', views.users_profile, name='profile'),
    path('update_profile', views.update_user, name='update_profile'),
    path('project/<int:pk>', views.view_project, name='project'),
    path('newproject/', views.new_project, name='new_project'),
    # path('api', ProjectListApiView.as_view()),


]