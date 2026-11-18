
from fastapi import APIRouter, Query

router = APIRouter(
    prefix="/api/v1",
    tags=["Mock API"]
)

MOCK_ARTICLES = [
    {
        "id": "mock-article-001",
        "category": "Local News",
        "headline": "Local development works begin in the mandal",
        "summary_60_words": (
            "Development works have started in the local area. "
            "Officials said the project will improve public "
            "facilities and benefit nearby residents."
        ),
        "cover_image_url": "https://example.com/news-image-1.jpg",
        "blurhash": "",
        "audio_url": "https://example.com/news-audio-1.mp3",
        "audio_duration_seconds": 45,
        "mandal_name": "Sample Mandal",
        "published_at": "2026-11-17T10:00:00Z",
        "is_breaking": False,
        "reporter": {"name": "Sample Reporter"},
        "stats": {"views": 125}
    },
    {
        "id": "mock-article-002",
        "category": "Politics",
        "headline": "Local representatives announce new public initiatives",
        "summary_60_words": (
            "Local representatives announced new initiatives "
            "to improve public services and infrastructure."
        ),
        "cover_image_url": "https://example.com/news-image-2.jpg",
        "blurhash": "",
        "audio_url": "https://example.com/news-audio-2.mp3",
        "audio_duration_seconds": 60,
        "mandal_name": "Sample Mandal",
        "published_at": "2026-11-17T11:00:00Z",
        "is_breaking": True,
        "reporter": {"name": "Sample Reporter"},
        "stats": {"views": 250}
    },
    {
        "id": "mock-article-003",
        "category": "Education",
        "headline": "Government school students participate in science fair",
        "summary_60_words": (
            "Students participated in a science fair showcasing "
            "creative projects and innovative ideas."
        ),
        "cover_image_url": "https://example.com/news-image-3.jpg",
        "blurhash": "",
        "audio_url": "https://example.com/news-audio-3.mp3",
        "audio_duration_seconds": 50,
        "mandal_name": "Sample Mandal",
        "published_at": "2026-11-17T12:00:00Z",
        "is_breaking": False,
        "reporter": {"name": "Sample Reporter"},
        "stats": {"views": 180}
    }
]


@router.get("/feed/home")
async def get_mock_home_feed(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100)
):
    total = len(MOCK_ARTICLES)

    start = (page - 1) * limit
    end = start + limit

    articles = MOCK_ARTICLES[start:end]

    return {
        "success": True,
        "data": articles,
        "meta": {
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": (total + limit - 1) // limit
        },
        "error": None
    }
