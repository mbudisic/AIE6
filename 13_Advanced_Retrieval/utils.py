import os
import getpass
from dotenv import load_dotenv

load_dotenv()
print("dotenv loaded")


def set_api_key_if_not_present(key_name, prompt_message=None):
    if key_name not in os.environ or not os.environ[key_name]:
        os.environ[key_name] = getpass.getpass(
            prompt_message if prompt_message else key_name
        )


"""
This module provides a class to render markdown text in Jupyter Notebooks using a pipe syntax.
"""

from IPython.display import display, Markdown


class MarkdownRenderer:
    """
    A class to render markdown text in Jupyter Notebooks using a pipe syntax.

    Example:
        md = MarkdownRenderer()
        "Hello *World*!" | md
    """

    def __ror__(self, other):
        """
        Overrides the right bitwise OR operator to display the given text as markdown.

        Args:
            other (str): The text to be rendered as markdown.
        """
        if isinstance(other, str):
            display(Markdown(other))
        else:
            # Optionally, handle non-string inputs, e.g., by converting them or raising an error
            display(Markdown(str(other)))
        # Return None or self, depending on whether you want the operation to be chainable
        # or produce a specific result. For display purposes, None is fine.
        return None


# Pre-instantiate for convenience if desired, so users can just import `markdown`
# from markdown_pipe import markdown_pipe (or a shorter name like `md`)
markdown_pipe = MarkdownRenderer()
