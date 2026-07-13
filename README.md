# pd-code-connected-sum

Join two oriented PD-code components and canonically renumber the result.

## Installation

```bash
pip install pd-code-connected-sum
```

## Quick start

`from pd_code_connected_sum import connected_sum` then `connected_sum(a, b, a_label, b_label)`.

PD codes are lists of four-entry crossings. Each arc label must occur exactly twice. Functions validate their inputs and do not mutate caller-owned PD-code lists unless explicitly documented.

## Development

Use Python 3.10 or newer for Python packages. Build distributions with `poetry build`. Run the package's tests or examples before publishing. C++ projects require a modern standards-compliant compiler.

## License

MIT. See `LICENSE`.
