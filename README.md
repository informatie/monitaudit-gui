# monitaudit-gui

A Streamlit-based graphical interface for exploring the MonitAudit error-code catalogue.

`monitaudit-gui` provides a simple, searchable interface for MonitAudit `MTA-*` error codes. It reads the machine-readable `monitaudit.errors` catalogue and makes error information easier to inspect without searching through configuration files manually.

## Features

- Browse all MonitAudit `MTA-*` error codes
- Search by error code, title, description, solution, exception, tag or runtime context
- Filter errors by category, severity and status
- View detailed error descriptions and recommended solutions
- Inspect associated exception types
- See whether an error is retryable
- View error lifecycle information
- Inspect expected runtime context fields
- Display the original YAML definition for each error
- Read the catalogue version and metadata directly from `monitaudit.errors`

## Error catalogue

The application reads:

`config/error/monitaudit.errors`

The catalogue is YAML-based and contains stable MonitAudit error definitions such as:

MTA-00419 · Environment configuration missing

Each error can contain:

- title
- category
- severity
- description
- solution
- exception
- retryable status
- lifecycle information
- runtime context fields
- tags

The `MTA-*` code provides the stable machine-readable identifier, while the catalogue provides the human-readable explanation and troubleshooting information.

## Purpose

MonitAudit runtime errors can remain concise:

MTA-00419: environment='qa'

`monitaudit-gui` can then be used to look up `MTA-00419` and display its full description, solution and technical metadata.

This keeps application logs compact while preserving detailed troubleshooting information in one central error catalogue.

## Running

```bash
uv run streamlit run app.py