from django.shortcuts import render
from . import util
from markdown import markdown
from django.utils.safestring import mark_safe


def convert_markdown_to_html(content):
    """
    Convert markdown content to HTML, ensuring links are properly rendered
    """
    # Convert markdown to HTML with the 'links' extension enabled
    html_content = markdown(content, extensions=["fenced_code", "tables", "footnotes"])

    # Mark the content as safe to prevent HTML escaping
    return mark_safe(html_content)


def index(request):
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
