# track-osc

A tool to track movement of objects and sent that information as OSC messages.

[Poetry](https://python-poetry.org/) is a tool to automatically take care of installing dependencies and running your python scripts. This template packages a simple python script which depends on additional libraries to run.

To run this application you need to install [poetry](https://python-poetry.org). The easiest way is to install it via [pipx](https://pipx.pypa.io) (to see how install pipx see [here](https://pipx.pypa.io/stable/installation/)). With pipx installed, to install poetry run the following code:

```
pipx install poetry
``` 

To run this application do:

```
poetry install
poetry run track-osc
```

To package the application with pyinstaller creating a stand-alone executable do:

```
poetry run build-exe
```

The executable will be `dist/track-osc` or `dist/track-osc.exe`

## vscode

To select the virtualenv created by poetry in vscode click on the virtualenv selection dropdown at the bottom of the edit window and select the entry which has "poetry" on the right.
