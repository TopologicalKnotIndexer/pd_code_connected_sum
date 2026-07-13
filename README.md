# pd-code-connected-sum

Join two selected oriented PD-code components and canonically renumber the result.

## Installation

```bash
pip install pd-code-connected-sum
```

## Usage example

```python
from pd_code_connected_sum import connected_sum

left = [[1, 5, 2, 4], [3, 1, 4, 6], [5, 3, 6, 2]]
right = [[1, 5, 2, 4], [3, 1, 4, 6], [5, 3, 6, 2]]
result, label_map = connected_sum(left, right, 1, 1)
print(result)
print(label_map["a_1"], label_map["b_1"])
```

## Algorithm

Each input component is converted to a deterministic oriented cycle. The algorithm locates the incidence immediately after each selected arc, offsets the second code to avoid collisions, cuts those two oriented arcs, and glues the endpoints crosswise. It then canonically orders component cycles, assigns contiguous labels, orients every crossing consistently, and returns maps for all original labels. This avoids the incorrect local crossing replacement used by older releases.

## Input conventions

A PD code is represented as a list of four-entry crossings. Arc labels normally occur exactly twice. Public functions validate inputs and return new values rather than mutating caller-owned data unless their API explicitly says otherwise.

## External software

No external software is required.

## Development

Run examples and package checks before release. Python packages require Python 3.10 or newer. Build PyPI artifacts with:

```bash
poetry check
poetry build
```

## License

MIT. See `LICENSE`.
