# tap-salesmate

`tap-salesmate` is a Singer tap for salesmate, I wrote this tap specifically to work with Target DBs like target-postgres.

Available Streams
- Activity
- Deals


Built with the Meltano [SDK](https://gitlab.com/meltano/singer-sdk) for Singer Taps.

## Configuration

### Accepted Config Options

- sessionToken
- start_date
- instance_name

A full list of supported settings and capabilities for this
tap is available by running:

```bash
tap-salesmate --about
```

## Usage

You can easily run `tap-salesmate` by itself or in a pipeline using [Meltano](www.meltano.com).

### Executing the Tap Directly

```bash
tap-salesmate --version
tap-salesmate --help
tap-salesmate --config CONFIG --discover > ./catalog.json
```

### Initialize your Development Environment

```bash
pipx install poetry
poetry install
```

### Create and Run Tests

Create tests within the `tap_salesmate/tests` subfolder and
  then run:

```bash
poetry run pytest
```

You can also test the `tap-salesmate` CLI interface directly using `poetry run`:

```bash
poetry run tap-salesmate --help
```

### SDK Dev Guide

See the [dev guide](https://gitlab.com/meltano/singer-sdk/-/blob/main/docs/dev_guide.md) for more instructions on how to use the SDK to 
develop your own taps and targets.
