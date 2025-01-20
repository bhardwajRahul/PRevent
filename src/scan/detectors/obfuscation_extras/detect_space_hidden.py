from typing import Optional


def detect_space_hiding(patch: str) -> Optional[dict]:
    index = patch.find(' ' * 170)
    if index != -1:
        start_idx = patch.rfind('\n', 0, index)  # Last newline before the match
        end_idx = patch.find('\n', index)  # Next newline after the match
        line = patch[start_idx + 1:end_idx]  # Cut between the surrounding newlines
        line_content = line.replace('  ', '')
        if len(line) > 170 and len(line_content) > 20:
            return {
                "message": "An unreasonable amount of spaces in line, probably for hiding",
                "line_number": patch.count('\n', 0, start_idx) + 1,  # Count newlines up to match's start
                "match": line_content
            }
    return None
