import re
import requests
from urllib.parse import urlparse, unquote
from .google_search_api import GoogleSearchAPI

class ProfilePicture(object):

    def __init__(self, key: str, cx: str):
        self._api_obj = GoogleSearchAPI(key, cx)

    def extract_id(self, link: str) -> str:
        """
            To get clean linkedin id
            Example: 
                Input  : linkedin.com/in/manuotel/
                Output : manuotel
        """
        linkedin_id = link
        match = re.findall(r'\/in\/([^\/]+)\/?', urlparse(link).path)
        if match:
            linkedin_id = match[0].strip()
        linkedin_id = linkedin_id.strip("/")
        linkedin_id = unquote(linkedin_id)
        return linkedin_id

    def _check_picture_url(self, link: str) -> bool:
        match = re.findall(r"(media-exp\d\.licdn\.com).+?(profile-displayphoto-shrink_)", link)
        return bool(match)

    def _check_url_exists(self, link):
        flag = False
        try:
            resp = requests.get(link, timeout=5)
            if resp and resp.status_code == 200:
                flag = True
        except:
            pass
        return flag

    def _extract_profile_picture(self, linkedin_id: str, res: list) -> str:
        link = ""
        for i in res:
            linkedin_url = i.get("link","")
            search_id = self.extract_id(linkedin_url)
            if search_id == linkedin_id:
                metatags = i["pagemap"]["metatags"][0]
                if "og:image" in metatags and "media.licdn.com" in metatags["og:image"]:
                    if self._check_url_exists(metatags["og:image"]):
                        link = metatags["og:image"]
                        break
        return link

    def search(self, link: str) -> object:
        linkedin_id = self.extract_id(link)
        api_resp = self._api_obj._hit_api(linkedin_id)
        api_resp.link = self._extract_profile_picture(linkedin_id, api_resp._search_results)
        api_resp.linkedin_id = linkedin_id
        return api_resp
