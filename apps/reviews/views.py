from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *

def index(request):
    return render(request, "reviews/index.html")


def register(request):
    result = User.objects.register_validator(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/')
    request.session['user_id'] = result.id
    messages.success(request, "Successfully registered!")
    return redirect('/success')


def login(request):
    result = User.objects.login_validator(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/')
    request.session['user_id'] = result.id
    messages.success(request, "Successfully logged in!")
    return redirect('/success')


def success(request):
    try:
        request.session['user_id']
    except KeyError:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user': user,
        'newest': Review.objects.order_by('created_at').reverse()[:3],
        'the_rest': Review.objects.order_by('created_at').reverse()[3:]
    }
    return render(request, "reviews/welcome.html", context)


def add(request):
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user': user,
    }
    return render(request, "reviews/add.html", context)


def addBook(request):
    print request.session['user_id']
    user = User.objects.get(id=request.session['user_id'])
    # getbook = Book.objects.get(id=book_id)
    book = Book.objects.create(
        name = request.POST['name'],
        author = request.POST['author'],
        uploader = user,
    )
    review = Review.objects.create(
        content = request.POST['content'],
        rating = request.POST['stars'],
        reviewer = user,
        book_obj = book
    )
    # context = {
    #     "user" : user,
    #     "bookCreated" : book,
    #     "reviewCreated" : review,
    #     "linkedBook": getbook
    # }
    url = "/title/" + str(book.id)
    # return redirect(request, url)
    return redirect(url)
    # return render(request, "reviews/book.html", context)


def addReview(request):
    book = Book.objects.get(id=request.POST['bookid'])
    user = User.objects.get(id=request.session['user_id'])
    review = Review.objects.create(
        content = request.POST['addreview'],
        rating = request.POST['stars'],
        reviewer = user,
        book_obj = book
    )
    # context = {
    #     "reviewCreated" : review
    # }
    # return render("reviews/book.html", context)
    url = "/title/" + str(book.id)
    return redirect(url)



def showBook(request, book_id):
    bookToShow = Book.objects.get(id=book_id)
    context = {
        'book': bookToShow,
        'all_reviews': bookToShow.book_reviews.all()
    }
    return render(request, 'reviews/book.html', context)



def userpage(request, id):
    user = User.objects.get(id=id)
    review = Review.objects.filter(reviewer=user)
    count = review.count()
    print count
    context = {
        "user" : user,
        "reviewedBooks" : review,
        "countReviews": count
    }
    return render(request,'reviews/user.html', context)


def destroy(request, review_id):
    review = Review.objects.get(id=review_id)
    goback = '/title/' + str(review.book_obj.id)
    if request.session['user_id'] == review.reviewer.id:
        review.delete()
    return redirect(goback)


def logout(request):
    context = {
        "logout" : request.session.pop("user_id")
        }
    return render(request, "reviews/index.html", context)