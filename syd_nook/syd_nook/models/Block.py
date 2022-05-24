from abc import ABC, abstractmethod
import datetime
import json

with open("syd_nook/models/conversions.json") as f:
    conversions_json = json.load(f)

class Block(ABC):
    conversions = conversions_json

    @abstractmethod
    def __init__(self, block: dict):
        """
        Notion content block

        :param block: JSON dict of block element
        """
        self.id: str = block["id"]
        self.date_edited = datetime.datetime.strptime(block["last_edited_time"], "%Y-%m-%dT%H:%M:%S.%fZ")
        self.block_type: str = block["type"]
        self.elem_type: str = self.type_to_html_elem(self.block_type)
        self.properties = dict()
    
    def type_to_html_elem(self, block_type: str):
        """
        Convert block type to HTML element tag

        :param block_type: Type of Notion block
        :returns: HTML element tag as string
        """
        return self.conversions[block_type]["html"]

    def get_as_html(self):
        """
        Get block as html element

        :returns: block as string html element
        """
        # Get HTML element properties as a string
        prop_string = str()
        for property in self.properties:
            value = self.properties[property]
            prop_string += f' {property}="{value}"'

        return f"<{self.elem_type}{prop_string}>{self.content}</{self.elem_type}>"

class TextBlock(Block):
    def __init__(self, block: dict):
        """
        Block of text

        :param block: block as dict
        """
        super(TextBlock, self).__init__(block)

        # Text content
        rich_text = block[self.block_type]["rich_text"]
        if len(rich_text) == 0:
            rich_text: dict = dict()
            self.content: str = ""
        else:
            rich_text: dict = rich_text[0]
            self.content: str = rich_text["plain_text"]

        # Get text annotations
        self.annotations: dict = rich_text.get("annotations", {})

        # Get href if any, and add it as property if appropriate
        self.href: str = rich_text.get("href", "")
        if type(self.href) == str:
            if len(self.href) > 0:
                self.properties["href"] = self.href
                self.properties["target"] = "_blank"
                self.elem_type = "a"

class ImageBlock(Block):
    def __init__(self, block: dict):
        """
        Image block

        :param block: block as dict
        """
        super(ImageBlock, self).__init__(block)

        self.src: str = block["image"]["file"]["url"]
        self.properties["src"] = self.src
        self.content = ""

class TableBlock(Block):
    def __init__(self, block: dict, rows: list[dict]):
        """
        Table block

        :param block: block as dict
        :param rows: list of table row elements as dict
        """
        super(TableBlock, self).__init__(block)

        self.rows: list[TableRowBlock] = [TableRowBlock(row_block) for row_block in rows]
        self.content = "".join([row.get_as_html() for row in self.rows])

class TableRowBlock(Block):
    def __init__(self, block: dict):
        """
        Table row block

        :param block: block as dict
        """
        super(TableRowBlock, self).__init__(block)

        self.content = list()

        cells = block["table_row"]["cells"]
        for cell in cells:
            if len(cell) > 0:
                table_data = cell[0]["plain_text"]
                self.content.append(table_data)
            else:
                self.content.append("")
            
        self.content = "".join(f"<td>{elem}</td>" for elem in self.content)

class OrderedListBlock(Block):
    def __init__(self, elems: list[dict]):
        """
        Block of ordered list elements

        :param elems: list of list elements as dict
        """
        self.blocks = [TextBlock(elem) for elem in elems]
        self.content = "".join([block.get_as_html() for block in self.blocks])
        self.elem_type = "ol"
        self.properties = {}
