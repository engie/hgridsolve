def print_3x3_grid(depth=0, content=None, highlight_cell=None ):
    """
    Prints a 3x3 ASCII grid to the console, with each cell 4 lines high:
      1) x,y coordinates (with trailing space)
      2) Custom content returned by content(x, y)
      3) Blank line
      4) Blank line

    :param depth: Number of spaces to indent each printed line.
    :param highlight_cell: A tuple (hx, hy) specifying the cell to highlight;
                           if None, no cell is highlighted.
    :param content: A function of the form content(x, y) -> str, used to 
                    generate the cell content line. If None, we use a default.

    Example usage:
        print_3x3_grid(
            depth=2, 
            highlight_cell=(1, 1),
            content=lambda x, y: f"Cell {x},{y} stuff"
        )
    """

    # Default content function if none is provided
    if content is None:
        content = lambda x, y: "A,B,C,D,E,F,G,H,I"

    indent = " " * depth

    CELL_WIDTH  = 24
    CELL_HEIGHT = 4

    # Build a horizontal separator line
    horizontal_line = "+" + ("-" * CELL_WIDTH + "+") * 3

    def pad_cell_text(text):
        """Pad text to the cell width."""
        return text + " " * (CELL_WIDTH - len(text))

    def highlight_text(text):
        """
        Simple highlight function.
        Wraps the text in >> and << to show highlighting.
        """
        return f">>{text}<<"

    # For each row in the grid
    for y in range(3):
        # Print the top border
        print(indent + horizontal_line)

        # For each line in the cell (CELL_HEIGHT lines)
        for row_in_cell in range(CELL_HEIGHT):
            row_text = []

            for x in range(3):
                # Determine if this cell is highlighted
                is_highlight = (highlight_cell is not None) and (x, y) == highlight_cell

                # Decide what base_text to display
                if row_in_cell == 0:
                    # First line: coordinates
                    base_text = f"{x},{y} "
                elif row_in_cell == 2:
                    # Second line: content function
                    base_text = content(x, y) + " "
                else:
                    # Lines 3 and 4 are blank
                    base_text = ""

                # Highlight if needed
                final_text = highlight_text(base_text) if is_highlight else base_text

                # Pad to the cell width
                cell_line_text = pad_cell_text(final_text)
                row_text.append("|" + cell_line_text)

            # End the row with a closing '|'
            row_text.append("|")
            print(indent + "".join(row_text))

    # Print the bottom border
    print(indent + horizontal_line)


if __name__ == "__main__":
    # Example usage:
    print_3x3_grid(
        depth=2, 
        highlight_cell=(1, 1),
        content=lambda x, y: f"CellContent({x},{y})"
    )