# track-osc

A tool to track movement of objects and sent that information as OSC messages.

# Running

## Binary

There is a released executable in Github releases

## Interpret the python code

You need to install python and uv.

Install Python 3 from [the official website](https://www.python.org/downloads/).

[uv](https://docs.astral.sh/uv/) is a tool to automatically take care of installing dependencies and running your python scripts. To run this application you need to install [uv](https://docs.astral.sh/uv/). The easiest way is to install it via [pipx](https://pipx.pypa.io) (to see how install pipx see [here](https://pipx.pypa.io/stable/installation/)).

With pipx installed, to install uv run the following code:

```
pipx install uv
``` 

To run this application do:

```
uv sync
uv run track-osc
```

To package the application with pyinstaller creating a stand-alone executable do:

```
uv run --extra dev build-exe
```

The executable will be `dist/track-osc` or `dist/track-osc.exe`

## Test tool (OSC client)

There is a simple OSC test client that simulates one object moving in a square.

Run it with:

```
uv run osc-test-client --ip 127.0.0.1 --port 8000 --id 1 --period 6 --fps 30
```

Arguments:

- `--ip`: OSC server IP (default `127.0.0.1`)
- `--port`: OSC server port (default `8000`)
- `--id`: Object id (default `1`)
- `--period`: Seconds to complete the square before deletion (default `6`)
- `--fps`: Updates per second (default `30`)

## vscode

To select the virtualenv created by uv in vscode click on the virtualenv selection dropdown at the bottom of the edit window and select the entry which has ".venv" on the right.
