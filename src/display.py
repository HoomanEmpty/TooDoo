"""Pretty terminal output for the task list.

Draws the tasks as a box-drawn table that fits the width of the terminal
(long titles / descriptions are wrapped). Colors are used only when the output
is a real terminal and the NO_COLOR environment variable is not set.
No third-party packages are needed.
"""
import os
import shutil
import sys
import unicodedata

DONE_MARK = "✅"
PENDING_MARK = "⬜"

MARK_WIDTH = 2     # both marks above take two terminal cells
MIN_COLUMN = 12    # a title / description column is never squeezed below this

# ANSI style codes
BORDER = "2"           # dim
HEADER = "1;36"        # bold cyan
NUMBER = "36"          # cyan
PENDING_TITLE = "1"    # bold
DONE_TEXT = "2;9"      # dim + strikethrough
DONE_DESCRIPTION = "2"


# ---------------------------------------------------------------------------
# Text measuring and wrapping
# ---------------------------------------------------------------------------

def _width(text):
    """Number of terminal cells ``text`` needs.

    Wide characters (CJK, emoji) count as 2; combining marks and invisible
    characters (for example the zero-width non-joiner used in Persian) as 0.
    """
    total = 0
    for char in text:
        if unicodedata.category(char) in ("Mn", "Me", "Cf"):
            continue

        total += 2 if unicodedata.east_asian_width(char) in ("W", "F") else 1

    return total


def _lines_of(text):
    """Split a value into its lines (always at least one)."""
    return str(text).replace("\t", " ").splitlines() or [""]


def _natural_width(text):
    return max(_width(line) for line in _lines_of(text))


def _take(text, width):
    """The longest beginning of ``text`` that fits in ``width`` cells (min. 1 char)."""
    used = 0
    end = 0
    for char in text:
        char_width = _width(char)
        if used + char_width > width and end > 0:
            break

        used += char_width
        end += 1

    return text[:end]


def _wrap(text, width):
    """Wrap ``text`` into lines that are at most ``width`` cells wide."""
    lines = []

    for paragraph in _lines_of(text):
        line = ""

        for word in paragraph.split():
            # A single word wider than the column is cut into pieces.
            while _width(word) > width:
                if line:
                    lines.append(line)
                    line = ""

                piece = _take(word, width)
                lines.append(piece)
                word = word[len(piece):]

            if not line:
                line = word
            elif _width(line) + 1 + _width(word) <= width:
                line += " " + word
            else:
                lines.append(line)
                line = word

        lines.append(line)

    return lines


# ---------------------------------------------------------------------------
# Colors
# ---------------------------------------------------------------------------

def _use_color():
    """Colors only for a real terminal, and never if NO_COLOR is set."""
    if "NO_COLOR" in os.environ or os.environ.get("TERM") == "dumb":
        return False

    if not sys.stdout.isatty():
        return False

    if os.name == "nt":
        os.system("")  # switches on ANSI escape codes in the Windows console

    return True


def _make_painter(enabled):
    def paint(text, code):
        if enabled and text:
            return f"\033[{code}m{text}\033[0m"

        return text

    return paint


# ---------------------------------------------------------------------------
# The table
# ---------------------------------------------------------------------------

def _column_widths(tasks, number_width, terminal_width):
    """Pick the width of the title and description columns so the table fits."""
    title_natural = max([_natural_width("Task")] +
                        [_natural_width(task["title"]) for task in tasks])
    description_natural = max([_natural_width("Description")] +
                              [_natural_width(task["description"]) for task in tasks])

    # 4 columns: 3 separators of " │ " plus the outer "│ " and " │"
    borders = 3 * 3 + 4
    available = terminal_width - borders - number_width - MARK_WIDTH

    if title_natural + description_natural <= available:
        return title_natural, description_natural

    # Too wide: share the space, giving the title a bit less than the description.
    title = min(title_natural, max(available * 2 // 5, MIN_COLUMN))
    description = min(description_natural, max(available - title, MIN_COLUMN))
    title = min(title_natural, max(available - description, MIN_COLUMN))

    return title, description


def print_tasks(tasks):
    """Print the list of tasks (dicts) as a table followed by a short summary."""
    paint = _make_painter(_use_color())

    number_width = max(len(str(len(tasks))), 1)
    terminal_width = shutil.get_terminal_size((80, 24)).columns
    title_width, description_width = _column_widths(tasks, number_width, terminal_width)
    widths = [number_width, MARK_WIDTH, title_width, description_width]

    bar = paint("│", BORDER)

    def border_line(left, middle, right):
        line = left + middle.join("─" * (width + 2) for width in widths) + right
        return paint(line, BORDER)

    def row_line(cells):
        return f"{bar} " + f" {bar} ".join(cells) + f" {bar}"

    def pad(text, width, painted, align="left"):
        spaces = " " * (width - _width(text))
        return spaces + painted if align == "right" else painted + spaces

    # --- header ---
    header = [
        pad("#", number_width, paint("#", HEADER), "right"),
        pad("✓", MARK_WIDTH, paint("✓", HEADER)),
        pad("Task", title_width, paint("Task", HEADER)),
        pad("Description", description_width, paint("Description", HEADER)),
    ]

    # --- body ---
    body = []
    for number, task in enumerate(tasks, start=1):
        done = task.get("task_done", False)
        title_lines = _wrap(task["title"], title_width)
        description_lines = _wrap(task["description"], description_width)
        height = max(len(title_lines), len(description_lines))

        title_style = DONE_TEXT if done else PENDING_TITLE
        description_style = DONE_DESCRIPTION if done else ""

        cells = []
        for i in range(height):
            number_text = str(number) if i == 0 else ""
            mark = (DONE_MARK if done else PENDING_MARK) if i == 0 else ""
            title = title_lines[i] if i < len(title_lines) else ""
            description = description_lines[i] if i < len(description_lines) else ""

            cells.append([
                pad(number_text, number_width, paint(number_text, NUMBER), "right"),
                pad(mark, MARK_WIDTH, mark),
                pad(title, title_width, paint(title, title_style)),
                pad(description, description_width,
                    paint(description, description_style) if description_style else description),
            ])

        body.append(cells)

    lines = [border_line("╭", "┬", "╮"), row_line(header), border_line("├", "┼", "┤")]
    for cells in body:
        lines.extend(row_line(cell_row) for cell_row in cells)

    lines.append(border_line("╰", "┴", "╯"))

    # --- summary ---
    total = len(tasks)
    done_count = sum(1 for task in tasks if task.get("task_done", False))
    noun = "task" if total == 1 else "tasks"
    lines.append(paint(f" {total} {noun} · {done_count} done · {total - done_count} pending",
                       BORDER))

    print("\n".join(lines))
