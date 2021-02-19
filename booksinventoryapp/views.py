from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import RegistrationForm, AddBookForm, AddBookDetailsForm, SearchForm, BookUpdateForm, BookInfoUpdateForm
from django.http import HttpResponse
from .models import Book, BookInfo
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.template.loader import get_template
from django.db.models import Q
from django.views.generic import ListView,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from . import forms


def register(request):
    if request.method =='POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("dashboard")

    else:
        form = RegistrationForm()

    arg = {'form':form}
    return render(request,'signup.html',arg)


def home(request):
    return render(request,'home.html')

@login_required
def dashboard(request):
    current_user = request.user
    seller_id = current_user.id
    bookseller = Book.objects.filter(seller=seller_id)

    books_per_page = 5
    paginator = Paginator(bookseller, books_per_page) # Show 5 books per page.(default)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    search_query = None
    search_query_other_seller = None
    search_is_empty = False

    if request.method == 'GET':
        search_form = SearchForm()
    if request.method == 'POST':
        search_form = SearchForm(request.POST)
        if search_form.is_valid(): 
            
            search_is_empty = True
            keyword = search_form.cleaned_data['keyword']
            checks = search_form.cleaned_data['checks']
            books_per_page = search_form.cleaned_data['books_per_page']

            if 'isbn' in checks:
                if keyword.isnumeric():
                    search_query = Book.objects.filter(isbn__contains = int(keyword)).filter(seller = User.objects.get(username=request.user))
                    paginator = Paginator(search_query, books_per_page) 
                    page_number = request.POST.get('page')
                    page_obj = paginator.get_page(page_number)
            if 'title' in checks:
                search_query = Book.objects.filter(title__icontains = keyword).filter(seller = User.objects.get(username=request.user) )
            if 'author' in checks:
                search_query = Book.objects.filter(author__contains = keyword).filter(seller = User.objects.get(username=request.user))
            if 'publisher' in checks:
                search_query = Book.objects.filter(publisher__contains = keyword).filter(seller = User.objects.get(username=request.user))
            if 'isbn' and 'title' in checks:
                if keyword.isnumeric():
                    search_query = Book.objects.filter(isbn__contains = int(keyword)).filter(seller = User.objects.get(username=request.user))
                else:
                    search_query = Book.objects.filter(title__contains = keyword).filter(seller = User.objects.get(username=request.user) )
            if 'isbn' and 'author' in checks:
                if keyword.isnumeric():
                    search_query = Book.objects.filter(isbn__contains = int(keyword)).filter(seller = User.objects.get(username=request.user))
                else:
                    search_query = Book.objects.filter(author__contains = keyword).filter(seller = User.objects.get(username=request.user))
            if 'isbn' and 'publisher' in checks:
                if keyword.isnumeric():
                    search_query = Book.objects.filter(isbn__contains = int(keyword)).filter(seller = User.objects.get(username=request.user))
                else:
                    search_query = Book.objects.filter(publisher__contains = keyword).filter(seller = User.objects.get(username=request.user) )
            if 'title' and 'author' in checks:
                search_query = Book.objects.filter(Q(title__contains = keyword) | Q(author__contains= keyword), seller = User.objects.get(username=request.user))
            if 'title' and 'publisher' in checks:
                search_query = Book.objects.filter(Q(title__contains = keyword) | Q(publisher__contains= keyword), seller = User.objects.get(username=request.user))
            if 'author' and 'publisher' in checks:
                search_query = Book.objects.filter(Q(author__contains = keyword) | Q(publisher__contains= keyword), seller = User.objects.get(username=request.user))
            if 'isbn' and 'title' and 'author' in checks:
                if keyword.isnumeric():
                    search_query = Book.objects.filter(isbn__contains = int(keyword)).filter(seller = User.objects.get(username=request.user))
                else:
                    search_query = Book.objects.filter(Q(title__contains = keyword) | Q(author__contains= keyword), seller = User.objects.get(username=request.user))
            if 'isbn' and 'title' and 'publisher' in checks:
                if keyword.isnumeric():
                    search_query = Book.objects.filter(isbn__contains = int(keyword)).filter(seller = User.objects.get(username=request.user))
                else:
                    search_query = Book.objects.filter(Q(title__contains = keyword) | Q(publisher__contains= keyword), seller = User.objects.get(username=request.user))
            if 'title' and 'author' and 'publisher' in checks:
                search_query = Book.objects.filter(Q(title__contains = keyword) | Q(quthor__contains = keyword) | Q(publisher__contains= keyword), seller = User.objects.get(username=request.user))
            if 'isbn' and 'title' and 'author' and 'publisher' in checks or not checks:
                if keyword.isnumeric():
                    search_query = Book.objects.filter(isbn__contains = int(keyword)).filter(seller = User.objects.get(username=request.user))
                else:
                    search_query = Book.objects.filter(Q(title__contains = keyword) | Q(author__contains = keyword) | Q(publisher__contains= keyword), seller = User.objects.get(username=request.user))
            paginator = Paginator(search_query, books_per_page) 
            page_number = request.POST.get('page')
            page_obj = paginator.get_page(page_number)

    context = {
        'current_user':current_user,
        'seller_id': seller_id,
        'bookseller':bookseller,
        'search_form': search_form,
        'search_is_empty': search_is_empty,
        'search_query':search_query,
        'page_obj': page_obj,
    }
    return render(request,'dashboard.html', context=context)


@login_required
def add_book(request):
    if request.method == 'GET':
        form = AddBookForm()
        bookInSeller = None
    if request.method == 'POST':
        form = AddBookForm(request.POST)
        if form.is_valid(): 
            Isbn = form.cleaned_data['isbn']
            Quantity = form.cleaned_data['quantity']
            Price = form.cleaned_data['price']
            book = Book.objects.filter(isbn=Isbn)
            current_user = request.user
            seller_id = current_user.id
            bookInSeller = Book.objects.filter(isbn=Isbn).filter(seller = User.objects.get(username=request.user))
            
            if bookInSeller:
                print('you already have this book')
            else:
                if book:
                    add_book_info = BookInfo(
                        quantity = Quantity,
                        price = Price
                    )
                    add_book_info.save()
                    book_details = Book.objects.filter(isbn=Isbn)
                    print('book with same isbn number is present')
                    
                    add_details_of_already_added_book = Book(
                        isbn = book_details[0].isbn,
                        seller = User.objects.get(username=request.user),
                        title = book_details[0].title,
                        author = book_details[0].author,
                        publisher = book_details[0].publisher,
                        publication_date = book_details[0].publication_date,
                        quantity_and_price = add_book_info,
                        cover_page = book_details[0].cover_page
                    )
                    add_details_of_already_added_book.save()
                    return redirect("dashboard")

                else: 
                    print('book not present')
                    return redirect('add_book_details', isbn = Isbn, seller = seller_id, quantity = Quantity, price = Price)

    context = {
        'form':form,
        'bookInSeller': bookInSeller,
    }
    return render(request, 'add_book.html', context = context)

@login_required
def add_book_details(request, isbn, seller, quantity , price):
    if request.method == 'GET':
        form = AddBookDetailsForm()
    if request.method =='POST':
        form = AddBookDetailsForm(request.POST, request.FILES)
        print(form.is_valid())
        if form.is_valid():
            add_book_info = BookInfo(
                quantity = quantity,
                price = price
            )
            add_book_info.save()
            form = form.save(commit=False)
            form.isbn = isbn
            current_user = User.objects.get(username=request.user)
            form.seller = current_user
            form.quantity_and_price = add_book_info
            form.save()
            return redirect("dashboard")
            print(2)
    context = {'isbn':isbn,'seller': seller,'quantity': quantity, 'price': price, 'form':form}
    return render(request, 'add_book_details.html',context= context)


class BookListView(LoginRequiredMixin,ListView):
    model = Book
    paginate_by = 4
    template_name = "book_list.html"

    def get_queryset(self):
        return Book.objects.filter(seller=self.request.user.id).order_by('title')

class BookDetailView(LoginRequiredMixin,DetailView):
    model = Book
    template_name = "book_detail.html"

class BookDelete(LoginRequiredMixin,DeleteView):
    model = Book
    template_name = "book_confirm_delete.html"
    success_url = '/books/'

@login_required
def BookUpdate(request,id,quantity_and_price):
    book = Book.objects.get(pk=id)
    bookinfo = BookInfo.objects.get(pk=quantity_and_price)

    if request.method == 'GET':
        forms = (BookUpdateForm(request.POST or None, instance=book),BookInfoUpdateForm(request.POST or None,instance=bookinfo))
    
    if request.method == 'POST':
        forms = (BookUpdateForm(request.POST or None,  request.FILES or None, instance=book),BookInfoUpdateForm(request.POST or None,instance=bookinfo))
        if forms[0].is_valid() and forms[1].is_valid():
            forms[0].save()
            forms[1].save()
            print(forms)
            book = Book.objects.get(pk=id)
            context = {
            'pk':id,
            'book':book,
            }
            return render(request, 'book_detail.html',context=context)
    context = {
        'forms':forms,
        }
    return render(request, 'book_form.html',context=context)