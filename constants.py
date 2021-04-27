from utils import Area, Filters
from dotenv import load_dotenv
import os


load_dotenv()

TESSERACT_EXE = os.environ.get('TESSERACT_PATH')
GAME_SOURCE = os.environ.get('GAME_SOURCE')
DRIVER_PATH = os.environ.get('LOCAL_CHROME_DRIVER_PATH')
BROWSER_PATH = os.environ.get('LOCAL_CHROME_EXECUTABLE_PATH')
DEBUG_MODE = os.environ.get('DEBUG_MODE') == 'true'

PLAYER_AXIS_Y = 0
BINARY_THRESHOLD = 254
CONNECTIVITY = 4

FILTERS = Filters(True, False, False, False)

PLAYER_AREA = Area(411, 420)
ENEMY_AREA = Area(101, 400)
MISSILE_AREA = Area(30, 100)
