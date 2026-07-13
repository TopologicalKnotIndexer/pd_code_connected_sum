from copy import deepcopy

import pd_code_pre_nxt
import pd_code_sanity


def _normalize(pd_code: list[list[int]]) -> tuple[list[list[int]], dict[int, int]]:
    if not pd_code:
        return [], {}
    pre, nxt = pd_code_pre_nxt.get_pre_nxt(pd_code)
    old_to_new: dict[int, int] = {}
    next_label = 1
    for start in pd_code_pre_nxt.get_num_set(pd_code):
        if start in old_to_new:
            continue
        current = start
        while current not in old_to_new:
            old_to_new[current] = next_label
            next_label += 1
            current = nxt[current]

    normalized = [[old_to_new[label] for label in crossing] for crossing in pd_code]
    new_next = {old_to_new[label]: old_to_new[target] for label, target in nxt.items()}
    for index, crossing in enumerate(normalized):
        if new_next[crossing[0]] == crossing[2]:
            continue
        if new_next[crossing[2]] == crossing[0]:
            normalized[index] = crossing[2:] + crossing[:2]
        else:
            raise ValueError("crossing is inconsistent with component orientation")
    normalized.sort()
    if not pd_code_sanity.sanity(normalized):
        raise AssertionError("normalization produced an invalid PD code")
    return normalized, old_to_new


def normalize_pd_code(pd_code: list[list[int]]) -> tuple[list[list[int]], dict[int, int]]:
    """Return a canonically oriented, contiguously labelled copy and its map."""
    if not pd_code_sanity.sanity(pd_code):
        raise ValueError("invalid PD code")
    return _normalize(deepcopy(pd_code))


def _endpoint(pd_code, label, nxt, pre, want_after: bool) -> tuple[int, int]:
    slots = [(i, j) for i, crossing in enumerate(pd_code) for j, value in enumerate(crossing) if value == label]
    if len(slots) != 2:
        raise ValueError("connected-sum label must occur exactly twice")
    if nxt[label] == pre[label]:
        return slots[1 if want_after else 0]
    target = nxt[label] if want_after else pre[label]
    for i, j in slots:
        if pd_code[i][(j + 2) % 4] == target:
            return i, j
    raise ValueError("could not locate oriented endpoint for label")


def connected_sum(
    pd_code1: list[list[int]], pd_code2: list[list[int]], val_1: int, val_2: int
) -> tuple[list[list[int]], dict[str, int]]:
    """Join the oriented components containing ``val_1`` and ``val_2``."""
    for pd_code in (pd_code1, pd_code2):
        if not pd_code_sanity.sanity(pd_code):
            raise ValueError("invalid PD code")
        if any(isinstance(x, bool) or not isinstance(x, int) for crossing in pd_code for x in crossing):
            raise TypeError("connected_sum requires integer labels")

    if not pd_code1 or not pd_code2:
        normalized, mapping = _normalize(deepcopy(pd_code1 or pd_code2))
        prefix = "a_" if pd_code1 else "b_"
        return normalized, {prefix + str(old): new for old, new in mapping.items()}
    if sum(label == val_1 for crossing in pd_code1 for label in crossing) != 2:
        raise ValueError("val_1 must occur exactly twice in pd_code1")
    if sum(label == val_2 for crossing in pd_code2 for label in crossing) != 2:
        raise ValueError("val_2 must occur exactly twice in pd_code2")

    first = deepcopy(pd_code1)
    offset = max(label for crossing in first for label in crossing)
    second = [[label + offset for label in crossing] for crossing in deepcopy(pd_code2)]
    second_label = val_2 + offset
    pre_a, nxt_a = pd_code_pre_nxt.get_pre_nxt(first)
    pre_b, nxt_b = pd_code_pre_nxt.get_pre_nxt(second)
    ai, aj = _endpoint(first, val_1, nxt_a, pre_a, True)
    bi, bj = _endpoint(second, second_label, nxt_b, pre_b, True)

    first[ai][aj] = second_label
    second[bi][bj] = val_1
    normalized, mapping = _normalize(first + second)
    output_map = {"a_" + str(old): new for old, new in mapping.items() if old <= offset}
    output_map.update({"b_" + str(old - offset): new for old, new in mapping.items() if old > offset})
    return normalized, output_map
