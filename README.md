# FastAPI-Template/Example

This example does __NOT__ use async for crud

This is not really finished or good and shouldn't be used by anyone that wants a finished template.

_Made with python 3.10.0b1_
_(That's why the [websocket](https://github.com/aaugustin/websockets/issues/935) version is pulled from git directly)_
- - - -

### Usage

This uses [pipenv](https://pipenv.pypa.io) so...

```bash
pipenv install
```

```bash
cd ./FastAPI-Template/
```

```bash
pipenv install
```

Then run it using [uvicorn](https://www.uvicorn.org/) or

```bash
pipenv run python ./ProjectName/app/main.py
```

### TODO

- [ ] Make a version with omar
- [ ] Make a version with async crud
- [ ] Refactor project to not mix different code patterns
- [ ] Add something for docker
- [ ] Create a start file to start it directly
- [ ] Add custom error pages
- [ ] Make it a [cookiecutter](https://cookiecutter.readthedocs.io) template
- [ ] Add more type hinting
- [ ] Add proper logging functions
- [ ] Maybe don't use upper module name so adding to path is not needed?