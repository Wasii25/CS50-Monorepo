from . import util
from markdown import markdown
from django.utils.safestring import mark_safe
from django import forms
from django.shortcuts import render, redirect


class NewTaskForm(forms.Form):
    search = forms.CharField(label="Search")


def convert_markdown_to_html(content):
    """
    Convert markdown content to HTML, ensuring links are properly rendered
    """
    # Convert markdown to HTML with the 'links' extension enabled
    html_content = markdown(content, extensions=["fenced_code", "tables", "footnotes"])

    # Mark the content as safe to prevent HTML escaping
    return mark_safe(html_content)


def index(request):
    print(util.list_entries)
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


def wiki(request, title):
    content = util.get_entry(title)  # Your existing function to get content
    if content is not None:
        html_content = convert_markdown_to_html(content)
        return render(
            request,
            "encyclopedia/wiki.html",
            {
                "title": title,
                "entry": html_content,
            },
        )
    else:
        return render(request, "encyclopedia/error.html", {"message": "Page not found"})


def search(request):
    if request.method == "POST":
        query = request.POST.get("q")  # Get the search query
        if query in util.list_entries():
            return redirect("wiki", title=query)  # Redirect to the wiki page
        # Handle case where page doesn't exist

        search_query_list = []
        for entry in util.list_entries():
            if query in entry:
                search_query_list.append(entry)

        if len(search_query_list) != 0:
            return render(
                request, "encyclopedia/search.html", {"entries": search_query_list}
            )

    return render(request, "encyclopedia/index.html")
