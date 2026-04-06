from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from notes_api import views as notes_views

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # API routes
    path('api/', include('notes_api.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Web interface routes
    path('', notes_views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('notes/', notes_views.NoteListView.as_view(), name='note_list'),
    path('notes/<int:pk>/', notes_views.NoteDetailView.as_view(), name='note_detail'),
    path('notes/create/', notes_views.NoteCreateView.as_view(), name='note_create'),
    path('notes/<int:pk>/edit/', notes_views.NoteUpdateView.as_view(), name='note_edit'),
    path('notes/<int:pk>/delete/', notes_views.NoteDeleteView.as_view(), name='note_delete'),
]
