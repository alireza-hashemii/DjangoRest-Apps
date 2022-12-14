from django.urls import path
from .views import *

app_name = 'watch_list'

urlpatterns = [
    path('movies/all',MovieWatchList.as_view(),name='movies-list'),
    path("movie/<int:pk>",MovieWatchDetail.as_view(),name="one_movie"),
    path('stream/all',Stream_Platform.as_view(),name="streamall"),
    path('stream/<int:pk>',Single_Stream_Platform.as_view(),name="singlestream"),
    # path('reviews/',ReviewList.as_view(),name='reviews'),
    # path("review/<int:pk>",ReviewDetail.as_view(),name="singlereview")
    path("movie/<int:pk>/reviews",ReviewList.as_view(),name="movie_reviews"),
    path("review/<int:pk>",ReviewDetail.as_view(),name="review"),
    path("movie/<int:pk>/create-review",CreateMovieReview.as_view(),name="moviereviewcreate")
]
