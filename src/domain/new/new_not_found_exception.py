class NewNotFoundException(Exception):
    def __init__(self, title: str):
        self.title = title
        super().__init__(f"New with title {title} not found")
