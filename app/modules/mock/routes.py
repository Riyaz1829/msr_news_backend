
from fastapi import APIRouter

router = APIRouter(
    prefix="/api/v1",
    tags=["Mock API"]
)


@router.get("/feed/home")
async def get_mock_home_feed():

    return {
        "success": True,
        "data": [
            {
                "id": "mock-article-001",
                "category": "Local News",
                "headline": "Local development works begin in the mandal",
                "summary_60_words": (
                    "Development works have started in the local area. "
                    "Officials said the project will improve public "
                    "facilities and benefit nearby residents. "
                    "Further updates will be shared after the work "
                    "progresses."
                ),
                "cover_image_url": "https://example.com/news-image.jpg",
                "blurhash": "",
                "audio_url": "https://example.com/news-audio.mp3",
                "audio_duration_seconds": 45,
                "mandal_name": "Sample Mandal",
                "published_at": "2026-11-17T10:00:00Z",
                "is_breaking": False,
                "reporter": {
                    "name": "Sample Reporter"
                },
                "stats": {
                    "views": 125
                }
            }
        ],
        "meta": {
            "page": 1,
            "limit": 20
        },
        "error": None
    }
