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

Each input is first converted to deterministic oriented cycles with contiguous temporary labels. The algorithm locates the incidence immediately after each selected arc, offsets the normalized second code to avoid collisions even when raw labels are negative or sparse, cuts those two oriented arcs, and glues the endpoints crosswise. It then canonically orders component cycles, assigns final contiguous labels, orients every crossing consistently, and returns maps for all original labels. This avoids both raw-label collisions and the incorrect local crossing replacement used by older releases.

## Input conventions

A PD code is represented as a list of four-entry crossings. Arc labels normally occur exactly twice. Public functions validate inputs and return new values rather than mutating caller-owned data unless their API explicitly says otherwise.

## External software

No external software is required.

## Development

Python 3.10 or newer is required. Run tests with the declared
`pd_code_sanity` and `pd_code_pre_nxt` dependencies available:

```bash
python -m unittest discover -s tests -v
```

No PyPI publication is performed as part of repository maintenance.

## License

MIT. See `LICENSE`.

## Citation

If you use this repository in academic work, please cite it as:

```bibtex
@software{topologicalknotindexer_pd_code_connected_sum,
  author = {{TopologicalKnotIndexer contributors}},
  title = {{pd\_code\_connected\_sum}},
  year = {2026},
  url = {https://github.com/TopologicalKnotIndexer/pd_code_connected_sum}
}
```
