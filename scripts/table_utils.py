"""Minimal table printer for heterogeneous dict rows."""
import json
import shutil


def _stringify(value, max_width):
    if value is None:
        return ""
    if isinstance(value, (dict, list)):
        s = json.dumps(value, separators=(",", ":"), default=str)
    else:
        s = str(value)
    s = s.replace("\n", " ").replace("\r", " ")
    if len(s) > max_width:
        s = s[: max_width - 1] + "…"
    return s


def print_table(rows, preferred=None, max_col_width=40, max_rows=None, all_columns=False):
    """Print a text table built from a list of dicts.

    - Unions keys across all rows so heterogeneous shapes are handled.
    - When `preferred` is given and `all_columns` is False, only those keys
      are shown (acts as a whitelist). Pass `all_columns=True` to include
      every key seen across the rows.
    - Columns that are empty across every row are dropped.
    - Nested values are rendered as compact JSON.
    """
    if not rows:
        print("(no rows)")
        return

    preferred = preferred or []
    seen = set()
    cols = []

    for key in preferred:
        if any(key in r for r in rows) and key not in seen:
            cols.append(key)
            seen.add(key)

    if all_columns or not preferred:
        for row in rows:
            for key in row.keys():
                if key not in seen:
                    cols.append(key)
                    seen.add(key)

    # Drop columns that are empty everywhere
    cols = [c for c in cols if any(
        row.get(c) not in (None, "", [], {}) for row in rows
    )]

    if not cols:
        print("(rows had no displayable fields)")
        return

    if max_rows and len(rows) > max_rows:
        display_rows = rows[:max_rows]
        truncated = len(rows) - max_rows
    else:
        display_rows = rows
        truncated = 0

    term_width = shutil.get_terminal_size((120, 20)).columns

    str_rows = [
        [_stringify(r.get(c), max_col_width) for c in cols]
        for r in display_rows
    ]

    widths = [len(c) for c in cols]
    for row in str_rows:
        for i, cell in enumerate(row):
            if len(cell) > widths[i]:
                widths[i] = len(cell)

    # Shrink columns proportionally if we exceed terminal width
    sep = "  "
    total = sum(widths) + len(sep) * (len(cols) - 1)
    if total > term_width:
        overflow = total - term_width
        shrinkable = sorted(range(len(cols)), key=lambda i: -widths[i])
        for i in shrinkable:
            if overflow <= 0:
                break
            reducible = max(widths[i] - 8, 0)
            cut = min(reducible, overflow)
            widths[i] -= cut
            overflow -= cut

    def fmt_row(cells):
        out = []
        for cell, w in zip(cells, widths):
            if len(cell) > w:
                cell = cell[: max(w - 1, 1)] + "…"
            out.append(cell.ljust(w))
        return sep.join(out)

    header = fmt_row(cols)
    print(header)
    print("-" * len(header))
    for row in str_rows:
        print(fmt_row(row))

    if truncated:
        print(f"... ({truncated} more rows not shown)")


def print_records(rows, max_rows=None):
    """Print each row as a vertical key: value block. Good for wide records."""
    if not rows:
        print("(no rows)")
        return

    display_rows = rows[:max_rows] if max_rows else rows
    for i, row in enumerate(display_rows, 1):
        print(f"\n[{i}/{len(rows)}]")
        if not isinstance(row, dict):
            print(f"  {row}")
            continue
        key_width = max((len(str(k)) for k in row.keys()), default=0)
        for k, v in row.items():
            if isinstance(v, (dict, list)):
                v = json.dumps(v, separators=(",", ":"), default=str)
            print(f"  {str(k).ljust(key_width)} : {v}")

    if max_rows and len(rows) > max_rows:
        print(f"\n... ({len(rows) - max_rows} more rows not shown)")


def offer_more_views(rows, preferred):
    """Prompt the user for follow-up views (all columns / vertical / JSON)."""
    if not rows:
        return
    while True:
        choice = input(
            "\nView more? [a]ll columns  [v]ertical detail  [j]son  [enter]=done: "
        ).strip().lower()
        if choice == 'a':
            print()
            print_table(rows, preferred=preferred, all_columns=True)
        elif choice == 'v':
            print_records(rows)
        elif choice == 'j':
            print(json.dumps(rows, indent=2, default=str))
        else:
            return
