from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect

from .forms import QuoteForm, AuthorForm, ScrapForm
from .models import Tag, Quote, Author
from .utils import Scrap


def get_top_tags():
    top_tags = Tag.objects.annotate(num_quotes=Count("quote")).order_by("-num_quotes")[
        :10
    ]
    font_sizes = [28, 26, 26, 24, 22, 14, 10, 8, 8, 6]
    for i, tag in enumerate(top_tags):
        tag.font_size = font_sizes[i]
    return top_tags


def main(request, page=1):
    top_tags = get_top_tags()
    quotes = Quote.objects.all()
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)
    return render(
        request,
        "quoteapp/index.html",
        context={"quotes": quotes_on_page, "top_tags": top_tags},
    )


def quotes_by_tag(request, tag_name, page=1):
    top_tags = get_top_tags()
    tag = get_object_or_404(Tag, name=tag_name)
    quotes = Quote.objects.filter(tags=tag)
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)
    return render(
        request,
        "quoteapp/tag.html",
        {"tag": tag, "quotes": quotes_on_page, "top_tags": top_tags},
    )


def author_detail(request, author_name):
    author = get_object_or_404(Author, fullname=author_name)
    return render(request, "quoteapp/author_detail.html", context={"author": author})


@login_required
def quote(request):
    tags = Tag.objects.all()
    all_authors = Author.objects.all()
    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_quote = form.save()
            choice_tags = Tag.objects.filter(name__in=request.POST.getlist("tags"))
            for tag in choice_tags.iterator():
                new_quote.tags.add(tag)
            new_quote.author = Author.objects.get(id=request.POST.get("author"))
            new_quote.save()

            return redirect(to="quoteapp:main")
        else:
            return render(
                request,
                "quoteapp/quote.html",
                {"tags": tags, "all_authors": all_authors, "form": form},
            )

    return render(
        request,
        "quoteapp/quote.html",
        {"tags": tags, "all_authors": all_authors, "form": QuoteForm()},
    )


@login_required
def author(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            new_author = form.save()
            new_author.save()

            return redirect(to="quoteapp:main")
        else:
            return render(
                request,
                "quoteapp/author.html",
                {"form": form},
            )

    return render(
        request,
        "quoteapp/author.html",
        {"form": AuthorForm()},
    )


@login_required()
def scrap(request):
    if request.method == "POST":
        form = ScrapForm(request.POST)
        if form.is_valid():
            scrapper = Scrap()
            url = "http://quotes.toscrape.com/"
            scrapper.run(url)

            return redirect(to="quoteapp:main")
        else:
            return render(
                request,
                "quoteapp/scrap.html",
                {"form": form},
            )

    return render(
        request,
        "quoteapp/scrap.html",
        {"form": ScrapForm()},
    )
