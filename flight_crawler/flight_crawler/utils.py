import re


def should_abort_requests(request):
    if not re.match(r"https://.*?flightradar24\.com", request.url):
        return True

    return (
        request.resource_type in ("image", "media", "font")
        or ".jpg" in request.url
    )
