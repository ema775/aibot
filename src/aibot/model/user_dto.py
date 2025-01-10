class UserDTO:
    """A Data Transfer Object (DTO) for the user information.

    Parameters
    ----------
    user_id : int
        The unique identifier of the user.

    """

    def __init__(self, user_id: int):
        self.user_id = user_id
