import html

def createHtmlElement(type, classname=None, id=None, style=None, content=None, text=None):
    class_attrib = f' class="{classname}"'
    id_attrib = f' id="{id}"'
    style_attrib = f' style="{style}"'
    return (f'<{type}'
            f'{class_attrib if classname is not None else ""}'
            f'{id_attrib if id is not None else ""}'
            f'{style_attrib if style is not None else ""}>'
            f'{content if content is not None else (html.escape(text) if text is not None else "")}'
            f'</{type}>')

print(createHtmlElement("span", text="Werbung <:)"))
print(createHtmlElement("div", classname="ad", id="teaser", style="width: 100%;", text="WERBUNG <:)"))
