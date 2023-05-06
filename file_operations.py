import textwrap


def write_wrapped_line(f, line, width=120):
    wrapped_lines = textwrap.fill(line, width=width)
    f.write(wrapped_lines + "\n")
