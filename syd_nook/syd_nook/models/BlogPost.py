from notion_client import Client
import datetime
from .Block import *
import json
import os

dirname = os.path.dirname(__file__)
with open(os.path.join(dirname, "conversions.json")) as f:
    conversions_json = json.load(f)

notion_secret = os.environ["NOTION_SECRET"]

notion = Client(auth=notion_secret)

class BlogPost:
    def __init__(self, post_id: str, is_thumbnail: bool = True, ):
        """
        Blog post object

        :param post_id: ID of post
        :kwarg is_thumbnail: option to add thumbnail (default: true)
        """
        self.id: str = post_id
        page: dict = notion.pages.retrieve(self.id)
        blocks_json: list = notion.blocks.children.list(post_id)["results"]

        self.title: str = Block.parse_rich_text(page["properties"]["Name"]["title"], as_html=False)
        self.description: str = Block.parse_rich_text(page["properties"]["Description"]["rich_text"], as_html=False)
        if is_thumbnail:
            self.thumbnail: str = page["properties"]["Thumbnail"]["files"][0]["file"]["url"]
            self.thumbnail_alt: str = Block.parse_rich_text(page["properties"]["Thumbnail Alt"]["rich_text"], as_html=False)
        self.status: str = page["properties"]["Status"]["select"]["name"]
        self.date_edited: datetime.date = datetime.datetime.strptime(page["last_edited_time"], "%Y-%m-%dT%H:%M:%S.%fZ")
        self.blocks: list = self._parse_blocks(blocks_json)
    
    def __str__(self):
        return self.title
    
    def get_blurb(self):
        """
        Get summary of blog post

        :returns: dict containing summary information
        """
        return {
            "title": self.title,
            "id": self.id,
            "date_edited": self.date_edited,
            "peek": self.description,
            "thumbnail": self.thumbnail,
            "thumbnail_alt": self.thumbnail_alt
        }

    def get_post_as_html(self):
        """
        Gets blog post as html

        :returns: string of blog post in html
        """
        return "".join([block.get_as_html() for block in self.blocks])

    def _parse_blocks(self, blocks_json: list):
        """
        Parse through list of blocks as dict

        :param blocks_json: blocks as dict
        :returns: blocks as Block object
        """
        result: list = list()
        open_ol: list = list()

        for ind, block in enumerate(blocks_json):
            is_list_open: bool = len(open_ol) > 0
            block_type: str = conversions_json[block["type"]].get("block_type")

            # If block is ordered list element, append to open ordered list
            is_numbered_list: bool = block_type == "numbered_list"
            if is_numbered_list:
                open_ol.append(block)

            # Close ordered list and push to result if its the end
            if (not is_numbered_list and is_list_open) or (is_numbered_list and ind + 1 == len(blocks_json)):
                result.append(OrderedListBlock(open_ol))
                open_ol = list()
            
            # If block is text, push TextBlock to result
            if block_type == "text":
                result.append(TextBlock(block))
            
            # If block is image, push ImageBlock to result
            if block_type == "image":
                result.append(ImageBlock(block))

            if block_type == "table":
                table_rows = notion.blocks.children.list(block["id"])["results"]
                result.append(TableBlock(block, table_rows))

        return result
