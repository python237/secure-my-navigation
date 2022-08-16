class CommandError(Exception):
    pass 


class CommandUnknown(CommandError):
    def __init__(command: str) -> None:
        super().__init__(f"{command} isn't a valid command.")
