from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import RegistrationForm, AddBookForm, AddBookDetailsForm, SearchForm
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

def register(request):
    if request.method =='POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            #form.password1 = make_password(form.cleaned_data['password1'])
            #print(form.password1)
            form.save()
            return redirect("dashboard")

    else:
        form = RegistrationForm()

    arg = {'form':form}
    return render(request,'signup.html',arg)


def home(request):
    # if auth
    # if logged in => redirect
    # else:
    return render(request,'home.html')

@login_required
def dashboard(request):
    current_user = request.user
    seller_id = current_user.id
    bookseller = Book.objects.filter(seller=seller_id)
    # for i in bookseller:
    #     print(i.isbn)
    # print(bookseller)

    # b= Book.objects.all()
    # print(b)

    #no_of_books = bookseller.count()
    # country = request.GET('countrySelect')
    # print(country)
    books_per_page = 5
    paginator = Paginator(bookseller, books_per_page) # Show 5 books per page.(default)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    search_query = None
    search_query_other_seller = None
    search_is_empty = False
    #seller = User.objects.get(id=request.user.id)
    #bookSellerHas = seller.mybooks.all()
    #print(bookSellerHas)
    if request.method == 'GET':
        search_form = SearchForm()
        #pagination_form = PaginationForm()
        
    
    if request.method == 'POST':
        search_form = SearchForm(request.POST)
        # pagination_form = PaginationForm(request.POST)

        # if pagination_form.is_valid():
        #     books_per_page = pagination_form.cleaned_data['books_per_page']
        #     paginator = Paginator(bookseller, books_per_page) # Show 2 books per page.
        #     page_number = request.GET.get('page')
        #     page_obj = paginator.get_page(page_number)

        if search_form.is_valid(): 
            
            search_is_empty = True
            keyword = search_form.cleaned_data['keyword']
            books_per_page = search_form.cleaned_data['books_per_page']
            checks = search_form.cleaned_data['checks']
            print(checks)
            paginator = Paginator(bookseller, books_per_page) # Show 2 books per page.
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            if 'isbn' in checks:
                if keyword.isnumeric():
                    search_query = Book.objects.filter(isbn__contains = int(keyword)).filter(seller = User.objects.get(username=request.user))
            if 'title' in checks:
                search_query = Book.objects.filter(title__contains = keyword).filter(seller = User.objects.get(username=request.user) )
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
            # if 'isbn' and 'title' and 'author' and 'publisher' in checks:
            if 'isbn' and 'title' and 'author' and 'publisher' in checks or not checks:
                if keyword.isnumeric():
                    search_query = Book.objects.filter(isbn__contains = int(keyword)).filter(seller = User.objects.get(username=request.user))
                else:
                    search_query = Book.objects.filter(Q(title__contains = keyword) | Q(author__contains = keyword) | Q(publisher__contains= keyword), seller = User.objects.get(username=request.user))


            # for i in checks:
            #     #print(i)
            #     if i == 'isbn':
            #         #print(int(book_title))
            #         # if book_title in bookseller.isbn:
            #         #     print(bookseller[0])

            #         # for k in bookseller:
            #         #     #print(str(k.isbn))
            #         #     s=str(k.isbn)
            #         #     if book_title in s:
            #         #         search_query = k 
            #         #         print(search_query)
                    
            #         search_query = Book.objects.filter(isbn__contains = int(book_title)).filter(seller = User.objects.get(username=request.user))
            #         print("search", search_query)
            #     elif i == 'title':
            #         print(i)
            #         search_query = Book.objects.filter(Q(title__contains = book_title) | Q(author__contains= book_title), seller = User.objects.get(username=request.user))
            #         print(search_query)
            #     elif i == 'author':
            #         search_query = Book.objects.filter(author__contains = book_title).filter(seller = User.objects.get(username=request.user))
            #     elif i == 'isbn' and i == 'title':
                    
            #     else:
            #         search_query = Book.objects.filter(author__contains = book_title).filter(seller = User.objects.get(username=request.user))
            

            # search_query = Book.objects.annotate(
            #     search=SearchVector('title__contains', 'author__contains'),
            # ).filter(search=book_title)

            #search_query = Book.objects.filter(title__contains = book_title).filter(seller = User.objects.get(username=request.user) )
            #print the books within seller inventory
            # if search_query:
            #     for i in search_query:
            #         print(i.seller.username)
            # #print the books other then seller's inventory
            # else:
            #     #search_query_other_seller = Book.objects.filter(title__contains = book_title)
            #     for i in search_query_other_seller:
            #         print(i.seller.username)

    context = {
        'current_user':current_user,
        'seller_id': seller_id,
        'bookseller':bookseller,
        'search_form': search_form,
        'search_is_empty': search_is_empty,
        'search_query':search_query,
        # 'search_query_other_seller': search_query_other_seller,
        'page_obj': page_obj,
    }
    return render(request,'dashboard.html', context=context)

@login_required
def your_books(request):
    bookseller = Book.objects.filter(seller=request.user.id)
    books_per_page = 5
    paginator = Paginator(bookseller, books_per_page) # Show 5 books per page.(default)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'bookseller':bookseller,
        'page_obj': page_obj,
    }
    return render(request,'your_books.html', context=context)


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
                    #print(book)
                    book_details = Book.objects.filter(isbn=Isbn)
                    #print(book_details)
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


        #print(form)
    context = {
        'form':form,
        'bookInSeller': bookInSeller,
    }
    return render(request, 'add_book.html', context = context)

@login_required
def add_book_details(request, isbn, seller, quantity , price):
    if request.method == 'GET':
        #print(QuantityAndPrice)
        form = AddBookDetailsForm()
    if request.method =='POST':
        #print(QuantityAndPrice,'this is quantity and price value')
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
            print("here")
            form.save()
            # return render(request,'dashboard.html')
            return redirect("dashboard")
            print(2)
    context = {'isbn':isbn,'seller': seller,'quantity': quantity, 'price': price, 'form':form}
    return render(request, 'add_book_details.html',context= context)

