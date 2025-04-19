from textnode import TextNode, TextType


def main():
    text_node = TextNode("I hate minorities", TextType.LINK, "https://pornhub.com")
    print(text_node)


if __name__ == "__main__":
    main()
