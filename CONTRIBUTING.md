# Contributing

Pull requests are welcome!

Feel free to open an issue if you found a bug, have new ideas, suggestions or found a mistake
in [documentation](https://python-telegram.readthedocs.io/en/latest/). 

## Reporting bugs

We use [GitHub
Issues](https://github.com/alexander-akhmetov/python-telegram/issues) to track
bugs. If you found a bug, please, open a new issue.

Try to include steps to reproduce and detailed description of the bug and maybe
some sample code.

## Pull request process

1. Fork the repository and create a new branch from `master`.
2. Make your changes and do not forget about new tests :)
3. Ensure the tests pass with your changes.
4. Create a new PR!


## Coding style

The project uses [black](https://github.com/psf/black) as a autoformatter tool
and checker and a few linters.

## Tests

To run tests you have to install [tox](https://tox.readthedocs.io/en/latest/).

Run tests:

```shell
tox
```

Run a specific test using python 3.7:

```shell
tox -e py37 -- -k test_add_message_handler
```
