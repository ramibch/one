import ipaddress

from django.conf import settings
from django.http import HttpRequest

from ..utils.telegram import Bot


class IpAddressMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        # Assign ip address to request
        request.ip_address = self.get_ip_address_or_none(request)
        return self.get_response(request)

    def get_ip_address_or_none(self, request) -> str | None:
        x_forwarded_for_ips = request.headers.get("X-Forwarded-For", "").split(", ")
        x_real_ip = request.headers.get("X-Real-Ip", "")
        remote_addr = request.META.get("REMOTE_ADDR", "")

        raw_addresses = (x_real_ip, *x_forwarded_for_ips, remote_addr)
        exempt_addresses = (None, "", "127.0.0.1", "localhost")
        addresses = {addr for addr in raw_addresses if addr not in exempt_addresses}
        ips = {ipaddress.ip_address(addr) for addr in addresses}

        ipsv4 = [str(ip) for ip in ips if ip.version == 4]
        ipsv6 = [str(ip) for ip in ips if ip.version == 6]

        if ipsv4:
            return ipsv4[0]
        if ipsv6:
            return ipsv6[0]

        if settings.ENV == "prod":
            Bot.to_admin(f"No IPv4 or IPv6 Addresses found for {request}\n{ips}")
