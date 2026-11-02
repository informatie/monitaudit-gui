# monitaudit-gui

A Streamlit-based graphical interface for exploring the MonitAudit error-code catalogue.

`monitaudit-gui` provides a searchable interface for MonitAudit `MTA-*` error codes. It reads the machine-readable `monitaudit.errors` catalogue and presents error descriptions, recommended solutions, exception metadata, lifecycle information, runtime context fields, and tags.

## Features

- Browse all MonitAudit `MTA-*` error codes
- Search by error code, title, description, solution, exception, tag, or runtime context
- Filter errors by category, severity, and status
- View detailed descriptions and recommended solutions
- Inspect associated exception types and retryability
- View lifecycle information, including introduction, deprecation, and replacement metadata
- Inspect expected runtime context fields
- Display the original YAML definition for each error
- Read catalogue version and metadata directly from `monitaudit.errors`

## Purpose

MonitAudit runtime errors can remain concise:

```text
MTA-00419: environment='qa'
```

`monitaudit-gui` can then be used to look up `MTA-00419` and display its full description, solution, and technical metadata. This keeps application logs compact while preserving detailed troubleshooting information in one central catalogue.

## Requirements

- Python 3.12 or later
- `uv`
- Streamlit
- PyYAML
- A valid MonitAudit error catalogue

## Installation

### Clone the repository

```bash
git clone <repository-url>
cd monitaudit-gui
```

Replace `<repository-url>` with the actual GitHub repository URL.

### Install the project

If the repository contains `pyproject.toml` and `uv.lock`:

```bash
uv sync
```

For a new project setup:

```bash
uv init
uv add streamlit pyyaml
uv add --dev ruff mypy pytest
```

### Verify the installation

```bash
uv run python -m py_compile app.py
uv run ruff check app.py
uv run mypy app.py
```

## Project structure

The expected project structure is:

```text
monitaudit-gui/
├── app.py
├── pyproject.toml
├── uv.lock
└── config/
    └── error/
        └── monitaudit.errors
```

## Configuration

The application reads the MonitAudit error catalogue from:

```text
config/error/monitaudit.errors
```

The path in `app.py` is:

```python
ERROR_CATALOGUE_PATH = Path(
    "config/error/monitaudit.errors"
)
```

Run the application from the repository root so this relative path resolves correctly.

Although the file is named `monitaudit.errors`, its contents use YAML syntax.

### Catalogue metadata

The catalogue begins with metadata:

```yaml
catalogue:
  name: MonitAudit
  version: 1.4.0
  code_prefix: MTA
  code_pattern: '^MTA-\d{5}$'
  resolution_policy: most_specific
```

### Error definitions

Error definitions are stored under the `errors` mapping:

```yaml
errors:
  MTA-00001:
    title: Invalid parameter
    category: general
    severity: error
    description: A parameter contains an invalid value.
    solution: Verify the parameter value and the calling procedure.
    exception: builtins.ValueError
    retryable: false
    status: active
    introduced: 1.4.0
    deprecated: null
    replaced_by: null
    documentation: null
    context:
      - parameter
      - value
    tags:
      - validation
      - parameter
```

The mapping key is the authoritative error identifier. Once an MTA code has been published, it must not be reused for a different condition.

### Runtime context

The `context` field defines which runtime values may accompany an error.

```yaml
MTA-00419:
  title: Environment configuration missing
  context:
    - environment
```

A runtime occurrence may then be represented as:

```text
MTA-00419: environment='qa'
```

Runtime values do not belong in `monitaudit.errors`; only their permitted field names are defined there.

### Error-code selection

Use the most specific error code available:

- FileSink write failure: `MTA-00705`
- JsonSink write failure: `MTA-00803`
- DeltaSink write failure: `MTA-00910`
- Unclassified custom sink failure: `MTA-00501`
- Unknown internal error: `MTA-09900` or `MTA-09999`

Application exceptions observed by MonitAudit tracing are not automatically converted into MTA errors. MTA codes identify MonitAudit failures, invalid MonitAudit inputs, or invalid MonitAudit configuration.

## Running the application

Start the GUI from the repository root:

```bash
uv run streamlit run app.py
```

Streamlit prints the local application address in the terminal.

## Using the GUI

The interface supports:

- full-text search
- direct lookup by `MTA-*` code
- category filtering
- severity filtering
- status filtering
- descriptions and recommended solutions
- exception and retryability metadata
- lifecycle information
- permitted runtime context fields
- tags
- raw YAML inspection

Example searches:

```text
MTA-00419
Delta
configuration
filesystem
sink
validation
```

## Updating the catalogue

When adding an error:

1. Select the correct reserved category range.
2. Allocate an unused `MTA-NNNNN` code.
3. Define the title, category, and severity.
4. Add a concise description.
5. Add an actionable solution.
6. Define the associated fully qualified exception, or `null` for diagnostic-only conditions.
7. Set whether the error is retryable.
8. Add lifecycle metadata.
9. Define permitted runtime context fields.
10. Add relevant tags.

Do not renumber existing published errors merely to keep codes sequential.

When retiring an error, keep the code and mark it as deprecated:

```yaml
status: deprecated
introduced: 1.4.0
deprecated: 2.0.0
replaced_by: MTA-00424
```

Reserved codes remain present with:

```yaml
status: reserved
```

## Development validation

Run the checks individually:

```bash
uv run python -m py_compile app.py
uv run ruff check .
uv run mypy .
uv run pytest
```

Or run the complete validation chain:

```bash
uv run python -m py_compile app.py && \
uv run ruff check . && \
uv run mypy . && \
uv run pytest
```

## Relationship with MonitAudit

`monitaudit-gui` is intentionally separate from the core MonitAudit package.

MonitAudit owns the MTA error-code taxonomy and machine-readable catalogue. `monitaudit-gui` provides the read-only visual interface for browsing, filtering, and understanding that catalogue.
