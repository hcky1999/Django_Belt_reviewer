from django.conf.urls import url 
from . import views              
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^success$', views.success),
    url(r'^add$', views.add),
    url(r'^addBook$', views.addBook),
    url(r'^addReview$', views.addReview),
    url(r'^users/(?P<id>\d+)$', views.userpage),
    url(r'^title/(?P<book_id>\d+)$', views.showBook),
    url(r'^destroy/(?P<review_id>\d+)$', views.destroy),

    # url(r'^$', views.welcome)     
]