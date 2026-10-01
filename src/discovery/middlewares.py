import requests
from scrapy.http import HtmlResponse

class CollabstrRequestsMiddleware:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://collabstr.com/",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
        })

    def process_request(self, request, spider):
        try:
            r = self.session.get(request.url, timeout=12)
            return HtmlResponse(
                url=request.url,
                status=r.status_code,
                body=r.content,
                encoding="utf-8",
                request=request
            )
        except Exception as e:
            spider.logger.error(f"Error downloading {request.url} via middleware: {e}")
            return None
