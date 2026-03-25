# Contributing

## Setup

1. Use Python 3.11+
2. Clone the repo
3. Run the app with `python main.py`
4. Run tests with `pytest -q`

## Code style

- Keep logic out of the UI layer when possible
- Add or update tests for every behavior change
- Keep the classic game rules intact unless the product scope changes

## Commit style

Use clear commit messages such as:

- `feat: improve round history panel`
- `test: add coverage for match reset`
- `docs: refresh setup instructions`

## Pull request expectations

- App still launches
- Existing tests pass
- New behavior includes test coverage when practical
- README stays accurate
