from .api import register_c3_api
from .TranscriptReader import TranscriptReader
from .SaveCourseData import SaveCourseData

# Flask API登録関数（Flaskがない場合は例外処理でスルー）
try:
    from .api import register_c3_api
    __all__ = [
        'register_c3_api',
        'TranscriptReader',
        'SaveCourseData',
    ]
except ImportError:
    __all__ = [
        'TranscriptReader',
        'SaveCourseData',
    ]
