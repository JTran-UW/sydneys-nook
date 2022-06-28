from django.shortcuts import render
from notion_client import Client
from .models.BlogPost import BlogPost
from django.http import Http404, HttpResponseBadRequest, JsonResponse

# TODO Change this!
notion_secret = "secret_Tch7KJPv1hUom2vXB9CnZMk9u6fo9XbKNVVZjSBKnUs"
kanban_id = "2dad4cbc8e154024998e64c33d2548e9"

notion = Client(auth=notion_secret)

# Create your views here.
def home(request):
    return render(request, "index.html")

def post_blurb(request, start_index, end_index):
    kanban = notion.databases.query(kanban_id, 
        filter={
            "property": "Status",
            "select": {
                "equals": "Done"
            }
        })

    blog_blurbs = []
    for page in kanban["results"]:
        post = BlogPost(page["id"])
        blog_blurbs.append(post.get_blurb())

    # Clean up weird request params
    if start_index:
        return HttpResponseBadRequest("start_index cannot exceed number of articles.")
    if end_index > len(blog_blurbs):
        end_index = len(blog_blurbs)

    return JsonResponse(blog_blurbs[start_index:end_index], safe=False)

def post_page(request, post_id):
    post = BlogPost(post_id)

    if post.status == "Done":
        return JsonResponse({
            "title": post.title, 
            "date_edited": post.date_edited,
            "post": post.get_post_as_html()
        })
    else:
        raise Http404
