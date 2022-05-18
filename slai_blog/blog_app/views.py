from django.shortcuts import render
from notion_client import Client
from .models import Article
from django.http import Http404

# TODO Change this!
notion_secret = "secret_Tch7KJPv1hUom2vXB9CnZMk9u6fo9XbKNVVZjSBKnUs"
kanban_id = "2dad4cbc8e154024998e64c33d2548e9"

notion = Client(auth=notion_secret)

# Create your views here.
def blog(request):
    kanban = notion.databases.query(kanban_id, 
        filter={
            "property": "Status",
            "select": {
                "equals": "Done"
            }
        })

    blog_blurbs = []
    for page in kanban["results"]:
        post_id = page["id"]
        blocks = notion.blocks.children.list(post_id)["results"]
        article = Article(page, blocks)
        blog_blurbs.append(article.get_blurb())

    return render(request, "blog_app/blog.html", {"blogs": blog_blurbs})

def post_page(request, post_id):
    page = notion.pages.retrieve(post_id)
    blocks = notion.blocks.children.list(post_id)['results']
    article = Article(page, blocks)

    if article.status == "Done":
        return render(request, "blog_app/post.html", {
            "title": article.title, 
            "blocks": article.get_article_as_html()
        })
    else:
        raise Http404
