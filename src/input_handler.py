"""A small helper that asks the user a question on the terminal and keeps
asking until the answer is valid.

Supported answer types: "str", "int" and "float".
"""

# Converters for the numeric answer types.
_NUMBER_TYPES = {"int": int, "float": float}

# Optional text transformations (``auto_prevention`` / ``rsls`` parameters).
_CASE_MODES = {"lower": str.lower, "upper": str.upper, "title": str.title}
_STRIP_MODES = {"rs": str.rstrip, "ls": str.lstrip, "rsls": str.strip}

_DEFAULT_ERROR = "\nThe answer was not accepted! - Expected answer(s): "


def _expand_options(options, numeric):
    """Turn the short ``options`` notation into a full list of valid answers.

    Numeric answers:
        [n]        -> 0 .. n
        [a, b]     -> a .. b

    Text answers (numbers are turned into strings):
        [n]            -> "0" .. "n"
        [titles]       -> titles
        [n, titles]    -> "0" .. "n" + titles   (the list may come first too)
        [a, b]         -> "a" .. "b"
        [a, b, titles] -> "a" .. "b" + titles

    Anything else is returned unchanged.
    """
    if numeric:
        if len(options) == 1:
            return list(range(options[0] + 1))
        if len(options) == 2:
            return list(range(options[0], options[1] + 1))
        return list(options)

    if len(options) == 1:
        first = options[0]
        if isinstance(first, list):
            return list(first)
        return [str(n) for n in range(first + 1)]

    if len(options) == 2:
        first, second = options
        if isinstance(first, list):
            return [str(n) for n in range(second + 1)] + first
        if isinstance(second, list):
            return [str(n) for n in range(first + 1)] + second
        return [str(n) for n in range(first, second + 1)]

    if len(options) == 3:
        start, stop, titles = options
        return [str(n) for n in range(start, stop + 1)] + list(titles)

    return list(options)


def _clean_text(answer, auto_prevention, rsls, rewrite):
    """Apply the optional case / whitespace / replace rules to a text answer."""
    if auto_prevention in _CASE_MODES:
        answer = _CASE_MODES[auto_prevention](answer)

    if rsls in _STRIP_MODES:
        answer = _STRIP_MODES[rsls](answer)

    if rewrite:  # (old, new)
        answer = answer.replace(rewrite[0], rewrite[1])

    return answer


def _in_range(value, low, high, brackets):
    """"[]" means both ends are allowed, "()" means both are excluded."""
    if brackets == "[]":
        return low <= value <= high
    return low < value < high


def input_handler(question="Value",
                  Type="str",
                  low_high=(float("-inf"), float("inf"), "[]"),
                  options=(),
                  default="",
                  auto_prevention="",
                  rsls="",
                  rewrite=(),
                  autofill=True,
                  option_error_message=_DEFAULT_ERROR):
    """Ask ``question`` until a valid answer is given and return it.

    question             -- text shown to the user
    Type                 -- "str", "int" or "float"
    low_high             -- (low, high, "[]" or "()") allowed range for numbers
    options              -- allowed answers (empty = anything); see _expand_options
    default              -- returned when the user just presses Enter
    auto_prevention      -- "lower", "upper" or "title": fix the case of text
    rsls                 -- "rs", "ls" or "rsls": strip whitespace (right/left/both)
    rewrite              -- (old, new): replace text inside the answer
    autofill             -- expand the short ``options`` notation
    option_error_message -- printed before the list of valid answers
    """
    is_number = Type in _NUMBER_TYPES
    if not is_number and Type != "str":
        raise ValueError(f"Unsupported Type: {Type!r}")

    low, high, brackets = low_high
    if is_number and brackets not in ("[]", "()"):
        raise ValueError('low_high[2] must be "[]" or "()"')

    # Expand the options once, not on every attempt.
    if autofill:
        options = _expand_options(options, is_number)

    while True:
        answer = input(question)
        if not answer:
            return default

        if is_number:
            try:
                value = _NUMBER_TYPES[Type](answer)
            except ValueError:
                print(" Invalid input ...")
                continue

            if not _in_range(value, low, high, brackets):
                print(f"\nOut of range! Please enter a value between "
                      f"{brackets[0]}{low}, {high}{brackets[1]}\n")
                continue
        else:
            value = _clean_text(answer, auto_prevention, rsls, rewrite)

        if options and value not in options:
            print(option_error_message, list(options))
            continue

        return value