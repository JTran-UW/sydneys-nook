import datetime
from notion_client import Client

notion_secret = "secret_Tch7KJPv1hUom2vXB9CnZMk9u6fo9XbKNVVZjSBKnUs"

notion = Client(auth=notion_secret)

class Block():
    conversions = {
        "heading_1": "h1",
        "heading_2": "h2",
        "heading_3": "h3",
        "paragraph": "p",
        "bulleted_list_item": "li",
        "numbered_list_item": "li"
    }

    def __init__(self, block):
        """
        Notion content block

        :param block: JSON dict of block element
        """
        self.id = block["id"]
        self.date_edited = datetime.datetime.strptime(block["last_edited_time"], "%Y-%m-%dT%H:%M:%S.%fZ")
        self.block_type = block["type"]
        self.elem_type = self.type_to_html_elem(self.block_type)

        # Text content
        rich_text = block[self.block_type]["rich_text"]
        self.is_newline = len(rich_text) == 0
        if self.is_newline:
            rich_text = dict()
            self.content = ""
        else:
            rich_text = rich_text[0]
            self.content = rich_text["plain_text"]

        # Annotations
        self.annotations = rich_text.get("annotations", {})
    
    def type_to_html_elem(self, block_type):
        """
        Convert block type to HTML element tag

        :param block_type: Type of Notion block
        :returns: HTML element tag as string
        """
        return self.conversions[block_type]

    def get_as_html(self):
        """
        Get block as html element

        :returns: block as string html element
        """
        return f"<{self.elem_type}>{self.content}</{self.elem_type}>"

class BlogPost:
    def __init__(self, post_id):
        """
        Blog post object

        :param page: JSON page information as dict
        :param blocks: JSON blocks information as list of dicts
        """
        self.id = post_id
        page = notion.pages.retrieve(self.id)
        blocks = notion.blocks.children.list(post_id)["results"]

        self.title = page["properties"]["Name"]["title"][0]["plain_text"]
        self.description = page["properties"]["Description"]["rich_text"][0]["plain_text"]
        self.status = page["properties"]["Status"]["select"]["name"]
        self.date_edited = datetime.datetime.strptime(page["last_edited_time"], "%Y-%m-%dT%H:%M:%S.%fZ")
        self.blocks = [Block(block) for block in blocks]
    
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
            "peek": self.description
        }

    def get_post_as_html(self):
        """
        TODO
        """
        open_list = False
        html_string = ""

        for ind, block in enumerate(self.blocks):
            is_ordered_list = block.block_type == "numbered_list_item"

            # Open an ordered list if there is an ol element
            if is_ordered_list and not open_list:
                html_string += "<ol>"
                open_list = True
            
            # Close an ordered list if final ol element
            if not is_ordered_list and open_list:
                html_string += "</ol>"
                open_list = False
            
            html_string += block.get_as_html()

            # Close an ordered list if at the end
            if ind + 1 == len(self.blocks):
                html_string += "</ol>"
                open_list = False
        
        return html_string

