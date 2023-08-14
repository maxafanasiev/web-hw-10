from django.urls import path

from . import views

app_name = "quoteapp"

urlpatterns = [
    path("", views.main, name="main"),
    path("<int:page>", views.main, name="main_paginate"),
    path("author/<str:author_name>", views.author_detail, name="author_detail"),
    path("tag/<str:tag_name>/", views.quotes_by_tag, name="quotes_by_tags"),
    path(
        "tag/<str:tag_name>/page/<int:page>/",
        views.quotes_by_tag,
        name="quotes_by_tags_paginate",
    ),
    path("quote/", views.quote, name="quote"),
    path("add-author/", views.author, name="author"),
    path("scrap/", views.scrap, name="scrap"),
]
