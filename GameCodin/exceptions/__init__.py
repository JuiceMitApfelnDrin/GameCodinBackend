class GameCodinException(Exception):
    msg: str
    status: int

    def __init__(self, msg: str, status: int = 400, *args: object) -> None:
        self.msg = msg
        self.status = status
        super().__init__(*args)