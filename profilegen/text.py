# Author: burncode
# Email: maohan0118@gmail.com
# Copyright (c) 2026 burncode
# License: MIT
"""Approximate font metrics for SVG layout without external packages.

Not pixel-perfect: actual fonts differ by operating system. Conservative bounds,
wrapping, and truncation avoid overflow for mixed CJK/Latin strings.
"""
import unicodedata


def units(text):
    total = 0.0
    for c in str(text):
        if unicodedata.combining(c):
            continue
        if unicodedata.east_asian_width(c) in ('W', 'F') or ord(c) >= 0x1F000:
            total += 2
        elif c in 'il.,:;!|\'` ':
            total += 0.8
        else:
            total += 1
    return total


def width(text, size):
    return units(text) * size * .64


def ellipsize(text, max_width, size):
    if width(text, size) <= max_width:
        return text
    suffix = '…'
    out = ''
    for c in text:
        if width(out + c + suffix, size) > max_width:
            break
        out += c
    return out + suffix


def wrap(text, max_width, size, max_lines=2):
    """Greedy Unicode-aware wrapping; last line is ellipsized when necessary."""
    text = str(text).strip()
    if not text:
        return []
    lines, line = [], ''
    for word in text.split(' '):
        candidate = (line + ' ' + word).strip()
        if width(candidate, size) <= max_width:
            line = candidate
            continue
        if line:
            lines.append(line)
            line = ''
        for char in word:
            if width(line + char, size) > max_width and line:
                lines.append(line)
                line = ''
            line += char
        if len(lines) >= max_lines:
            return lines[:max_lines-1] + [ellipsize(' '.join(lines[max_lines-1:] + ([line] if line else [])), max_width, size)]
    if line:
        lines.append(line)
    if len(lines) > max_lines:
        return lines[:max_lines-1] + [ellipsize(' '.join(lines[max_lines-1:]), max_width, size)]
    return lines
