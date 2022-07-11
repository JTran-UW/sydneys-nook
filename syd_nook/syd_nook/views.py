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

def about(request):
    return render(request, "about.html")

def post_blurb(request, start_index, end_index):
    query = request.GET.get("query", "")
    query_filter = {
        "property": "Status",
        "select": {
            "equals": "Done"
        },
    }

    if len(query) > 0:
        # Add OR statement
        query_filter = [query_filter, {
            "or": [{
                "property": "Name",
                "rich_text": {
                    "contains": query
                }
            },
            {
                "property": "Description",
                "rich_text": {
                    "contains": query
                }
            }]
        }]
        
        # Wrap in AND statement
        query_filter = {
            "and": query_filter
        }

    kanban = notion.databases.query(kanban_id, filter=query_filter)

    blog_blurbs = []
    for page in kanban["results"]:
        post = BlogPost(page["id"])
        blog_blurbs.append(post.get_blurb())

    max_reached = False

    # Clean up weird request params
    if start_index > len(blog_blurbs):
        return HttpResponseBadRequest("start_index cannot exceed number of articles.")
    if end_index > len(blog_blurbs):
        end_index = len(blog_blurbs)
        max_reached = True

    return JsonResponse({
        "maxReached": max_reached,
        "blurbs": blog_blurbs[start_index:end_index]
    }, safe=False)

def post_page(request, post_id):
    post = BlogPost(post_id)

    if post.status == "Done":
        return render(request, "post.html", {
            "title": post.title,
            "thumbnail": post.thumbnail,
            "date_edited": post.date_edited,
            "post": post.get_post_as_html()
        })
    else:
        raise Http404
