# from database.database import create_database, add_history, get_connection
from cli.cli_handler import cli

if __name__ == "__main__":
    # create_database()
    # add_history("hello world", 2, 11)
    # print([dict(r) for r in get_connection().execute("SELECT * FROM history")])

    cli()