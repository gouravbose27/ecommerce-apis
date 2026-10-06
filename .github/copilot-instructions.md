# E-commerce APIs

## Stack
- Python 3.13 for all implementation.
- FastAPI for all API endpoints.
- pytest for all unit tests.

## Environment
- Always install dependencies inside a virtual environment (`python3.13 -m venv .venv`, or `py -3.13 -m venv .venv` on Windows). Activate it before running `pip install`.
- Never install packages into the global interpreter.
- Record dependencies in `requirements.txt` (or `pyproject.toml`).

## Documentation
- Every function and method needs a docstring that includes at least one example usage (a `Example:` section or doctest-style `>>>` lines).

```python
def apply_discount(price: float, percent: float) -> float:
    """Return the price after applying a percentage discount.

    Example:
        >>> apply_discount(100.0, 10)
        90.0
    """
    return price * (1 - percent / 100)
```

## Testing
- Write unit tests with pytest in a `tests/` directory, named `test_*.py`.
- Test FastAPI endpoints with `fastapi.testclient.TestClient`.
- Run tests with `pytest` from the activated virtual environment.
