from typing import Any

from etsyv3 import EtsyAPI


class ExtendedEtsyAPI(EtsyAPI):
    """
    The Etsy API from https://github.com/anitabyte/etsyv3
    but methods which are not implemented.
    """

    def get_me(self) -> Any:
        """
        Remove if merged:
        https://github.com/anitabyte/etsyv3/pull/27
        """
        uri = f"{super().ETSY_API_BASEURL}/users/me"
        return self._issue_request(uri)
