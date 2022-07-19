from django.shortcuts import render
from notion_client import Client
from .models.BlogPost import BlogPost
from .models.Block import Block
from django.http import Http404, HttpResponseBadRequest, JsonResponse

# TODO Change this!
notion_secret = "secret_Tch7KJPv1hUom2vXB9CnZMk9u6fo9XbKNVVZjSBKnUs"
kanban_id = "2dad4cbc8e154024998e64c33d2548e9"
main_id = "291e9f3499824f7b9acc02ce4f17f30f"

notion = Client(auth=notion_secret)

def get_main_info():
    """
    Get main info

    :returns: dict of main info (title and subtitle)
    """
    main = notion.databases.query(main_id)["results"]
    main_info = {}

    for result in main:
        name = result["properties"]["Name"]["title"][0]["plain_text"]
        rich_text = result["properties"]["Content"]["rich_text"]
        content = Block.parse_rich_text(rich_text, as_html=False)
        
        "".join([text["plain_text"] for text in rich_text])

        main_info[name] = content

    return main_info

# Create your views here.
def home(request):
    kanban = notion.databases.query(kanban_id, filter={
        "property": "Status",
        "select": {
            "equals": "Special - Home"
        }
    })
    page = BlogPost(kanban["results"][0]["id"], is_thumbnail=False)
    content = {
        "title": page.title,
        "date_edited": page.date_edited,
        "description": page.description,
        "content": page.get_post_as_html()
    }
    main_info = get_main_info()

    return render(request, "index.html", {**content, **main_info})

def about(request):
    kanban = notion.databases.query(kanban_id, filter={
        "property": "Status",
        "select": {
            "equals": "Special - About"
        }
    })
    page = BlogPost(kanban["results"][0]["id"], is_thumbnail=False)
    content = {
        "title": page.title,
        "description": page.description,
        "post": page.get_post_as_html()
    }

    return render(request, "post.html", content)

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
        post_info = {
            "title": post.title,
            "description": post.description,
            "thumbnail": post.thumbnail,
            "thumbnail_alt": post.thumbnail_alt,
            "date_edited": post.date_edited,
            "post": post.get_post_as_html()
        }
        main_info = get_main_info()

        return render(request, "post.html", {**post_info, **main_info})
    else:
        raise Http404
