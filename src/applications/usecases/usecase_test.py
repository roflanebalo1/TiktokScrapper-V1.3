from src.adapters.driver_factory import DriverFactory 
from src.adapters.tiktoksessionrepository import TikTokSessionRepository
from src.adapters.load_cookies import LoadCookies
from src.adapters.parser import Parser

def Test(): 
    DriverFactory().create_driver
    TikTokSessionRepository()
    LoadCookies()
    Parser()