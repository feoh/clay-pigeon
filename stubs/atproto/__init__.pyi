from typing import Any as Any

class Client:
    def __init__(
        self, base_url: str | None = None, *args: Any, **kwargs: Any
    ) -> None: ...
    def login(
        self,
        login: str | None = None,
        password: str | None = None,
        session_string: str | None = None,
        auth_factor_token: str | None = None,
    ) -> Any: ...
