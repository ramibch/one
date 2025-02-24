from typing import Any

from etsyv3.etsy_api import ETSY_API_BASEURL, EtsyAPI, Method
from etsyv3.models.listing_request import UpdateListingRequest


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
        uri = f"{ETSY_API_BASEURL}/users/me"
        return self._issue_request(uri)

    def update_listing_deprecated(self, shop_id: int, listing_id: int, listing: UpdateListingRequest) -> Any:
        uri = f"{ETSY_API_BASEURL}/shops/{shop_id}/listings/{listing_id}"
        return self._issue_request(uri, method=Method.PUT, request_payload=listing)