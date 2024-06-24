# Contributing

Pull requests are welcome!

Feel free to open an issue if you find a bug, have new ideas, suggestions, 
or spot a mistake in the [documentation](https://python-telegram.readthedocs.io/en/latest/).

## Reporting bugs

We use [GitHub
Issues](https://github.com/alexander-akhmetov/python-telegram/issues) to track
bugs. If you find a bug, please open a new issue.

Try to include steps to reproduce the bug, a detailed description, and some sample code if possible.

## Pull request process

1. Fork the repository and create a new branch from `master`.
2. Make your changes and don't forget to add new tests :)
3. Ensure the tests pass with your changes.
4. Create a new PR!

## Coding style

The project uses [ruff](https://docs.astral.sh/ruff/) as an autoformatter and linter.

## Tests

To run tests you need to install [tox](https://tox.readthedocs.io/en/latest/).

Run tests:

```shell
tox
```

Run a specific test using python 3.12:

```shell
tox -e py312 -- -k test_add_message_handler
```
