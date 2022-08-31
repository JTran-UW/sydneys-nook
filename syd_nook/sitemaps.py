from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models.BlogPost import BlogPost
from notion_client import Client

import os

notion_secret = os.environ["NOTION_SECRET"]
kanban_id = os.environ["KANBAN_ID"]

notion = Client(auth=notion_secret)

class BlogSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7
    protocol = "https"

    def items(self):
        query_filter = {
            "property": "Status",
            "select": {
                "equals": "Done"
            },
        }
        kanban = notion.databases.query(kanban_id, filter=query_filter)

        posts = []
        for page in kanban["results"]:
            posts.append(BlogPost(page["id"]))

        return posts
    
    def lastmod(self, obj):
        return obj.date_edited
    
    def location(self, obj):
        return f"/blog/{obj.id}"

class StaticSitemap(Sitemap):
    changefreq = "yearly"
    priority = 1
    protocol = "https"

    def items(self):
        return ["home", "about"]

    def location(self, item):
        return reverse(item)
