from django.contrib import admin
from django.urls import path, re_path
from booksinventoryapp.views import register, home, login , dashboard, add_book, add_book_details, your_books
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', register, name='signup'),
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('add_book/', add_book, name='add_book'),
    path('your_books/', your_books, name='your_books'),
    path('add_book/<int:isbn>/<int:seller>/<int:quantity>/<int:price>', add_book_details, name='add_book_details'),
    #path('add_book/<int:isbn>', add_already_added_book, name='add_already_added_book')
    #re_path(r'^add_book/(?P<isbn>\d+)/(?P<seller>\d+)/$', add_book_details, name='add_book_details' ),
] + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
if settings.DEBUG: 
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)