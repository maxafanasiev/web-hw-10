from django.forms import ModelForm, CharField, TextInput, URLField

from .models import Quote, Author, Scrap_url


class QuoteForm(ModelForm):
    quote = CharField()

    class Meta:
        model = Quote
        fields = ["quote"]
        exclude = ["tags", "author"]


class AuthorForm(ModelForm):
    fullname = CharField(max_length=50, required=True, widget=TextInput())
    born_date = CharField(max_length=50)
    born_location = CharField(max_length=150)
    description = CharField()

    class Meta:
        model = Author
        fields = ["fullname", "born_date", "born_location", "description"]


class ScrapForm(ModelForm):
    # url = URLField(required=True)

    class Meta:
        model = Scrap_url
        exclude = ["url"]
