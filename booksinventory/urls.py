from django.contrib import admin
from django.urls import path, re_path
from booksinventoryapp.views import register, home, login , dashboard, add_book, add_book_details, BookListView, BookDetailView, BookUpdate, BookDelete
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static
# from .import views
#from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', register, name='signup'),
    path('', home, name='home'),
    # path('datapopulate/', DataPopulate, name='datapopulate'),
    path('dashboard/', dashboard, name='dashboard'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('add_book/', add_book, name='add_book'),
    # path('your_books/', BookListView.as_view(), name='your_books'),°
    path('books/', BookListView.as_view(), name='books'),
	path('book/<int:pk>',BookDetailView.as_view(), name='book-detail'),
    path('book/<int:id>/<int:quantity_and_price>/update/', BookUpdate, name='book_update'),
    path('book/<int:pk>/delete/', BookDelete.as_view(), name='book_delete'),
    path('add_book/<int:isbn>/<int:seller>/<int:quantity>/<int:price>', add_book_details, name='add_book_details'),
    #path('add_book/<int:isbn>', add_already_added_book, name='add_already_added_book')
    #re_path(r'^add_book/(?P<isbn>\d+)/(?P<seller>\d+)/$', add_book_details, name='add_book_details' ),
] 

if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)