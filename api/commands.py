import click

__all__ = (
    "api_cli",
)


@click.group("api")
def api_cli() -> None:
    pass


@api_cli.command()
def run_api() -> None:
    import uvicorn

    from api.app import app

    uvicorn.run(app, host="localhost", port=5000)
