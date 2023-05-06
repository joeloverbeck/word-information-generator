"""This module provides the ability to write a section of useful information for a word into a file, as HTML.

Functions:
write_section_to_file(file, title, items, use_table=False)

"""


def write_section_to_file(file, title, items, use_table=False):
    """Writes a formatted section with a title and a list of items to the specified file.

    Args:
        file (TextIOWrapper): The file to write to.
        title (str): The title of the section.
        items (list): A list of items to be displayed in the section.
        use_table (bool, optional): If True, the items will be displayed in a table format. Defaults to False.
    """
    if items:
        file.write(f"<h2>{title}</h2>\n")
        if use_table:
            file.write("<table>\n<tr>\n")
            for i, item in enumerate(items):
                file.write(f"<td>{item}</td>\n")
                if (i + 1) % 4 == 0:
                    file.write("</tr>\n<tr>\n")
            file.write("</tr>\n</table>\n\n")
        else:
            file.write("<ul>\n")
            for item in items:
                file.write(f"<li>{item}</li>\n")
            file.write("</ul>\n\n")
