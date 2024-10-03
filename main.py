import click


def prepare_cli() -> click.core.Group:
    from api.commands import api_cli

    main_cli = click.group()(lambda: None)
    main_cli.add_command(api_cli)

    return main_cli


def main() -> None:
    cli = prepare_cli()
    cli()


if __name__ == "__main__":
    main()
