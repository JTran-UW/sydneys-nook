from django.shortcuts import render
from notion_client import Client
from .models.BlogPost import BlogPost
from .models.Block import Block
from django.http import Http404, HttpResponseBadRequest, JsonResponse

# TODO Change this!
notion_secret = "INSERT"
kanban_id = "INSERT"
main_id = "INSERT"

notion = Client(auth=notion_secret)

def get_main_info(as_html_elems=False):
    """
    Get main info

    :kwarg as_html_elems: list of elements to return as html
    :returns: dict of main info (title and subtitle)
    """
    if not as_html_elems:
        as_html_elems = []

    main = notion.databases.query(main_id)["results"]
    main_info = {}

    for result in main:
        name = result["properties"]["Name"]["title"][0]["plain_text"]
        rich_text = result["properties"]["Content"]["rich_text"]

        as_html = name in as_html_elems
        content = Block.parse_rich_text(rich_text, as_html=as_html)
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
    main_info = get_main_info(as_html_elems=["SM_External"])

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
    main = get_main_info(as_html_elems=["SM_External"])

    return render(request, "post.html", {**content, **main})

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
        main_info = get_main_info(as_html_elems=["SM_External"])

        return render(request, "post.html", {**post_info, **main_info})
    else:
        raise Http404

# Post API Endpoint

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
