from selenium.webdriver.support import expected_conditions as EC
import json
from src.applications.dto import CookieDTO, CookieFileORMDTO
from src.infrastructure.models import TikTokSessionORM, TiktokHashtagsORM, TiktokSongsORM, TiktokBreakoutSongsORM
from src.applications.interfaces.interfaces import ITiktokSessionRepository

class TikTokSessionRepository(ITiktokSessionRepository):


    def load_cookies_from_db(self) -> CookieFileORMDTO:

        cookie_file = TikTokSessionORM.objects.first()

        if cookie_file is None:
            raise Exception("Нет записи CookieFileORM")
        
        cookies_content = cookie_file.content
        cookies_full_file = json.loads(cookies_content)
        cookie_dto = CookieFileORMDTO(cookies=cookies_full_file)

        return cookie_dto