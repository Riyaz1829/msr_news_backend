
from fastapi import APIRouter, Query

router = APIRouter(
    prefix="/api/v1",
    tags=["Mock API"]
)

MOCK_ARTICLES = [
    {
        "id": "550e8400-e29b-41d4-a716-446655440001",
        "category": "Local News",
        "headline": "Road improvement works begin in the mandal",
        "summary_60_words": (
            "Residents in the mandal welcomed the start of road "
            "improvement works near the main market and surrounding "
            "residential streets on Tuesday. Local officials said the "
            "project includes repairing damaged stretches, improving "
            "drainage points and adding safer pedestrian crossings. "
            "The work is expected to reduce travel delays for school "
            "students, traders and daily commuters. Authorities asked "
            "residents to follow temporary traffic diversions until "
            "construction is completed."
        ),
        "cover_image_url": "https://example.com/news-image-1.jpg",
        "blurhash": "",
        "audio_url": "https://example.com/news-audio-1.mp3",
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
    },
    {
        "id": "550e8400-e29b-41d4-a716-446655440002",
        "category": "Education",
        "headline": "Government school students participate in science exhibition",
        "summary_60_words": (
            "Government school students from several villages took "
            "part in a mandal-level science exhibition, presenting "
            "models on water conservation, renewable energy and waste "
            "management. Teachers said the event encouraged practical "
            "learning and helped students explain how science can "
            "address everyday community problems. Education officials "
            "visited the displays and appreciated the participants. "
            "Selected projects will be considered for the district-level "
            "exhibition scheduled later this month."
        ),
        "cover_image_url": "https://example.com/news-image-2.jpg",
        "blurhash": "",
        "audio_url": "https://example.com/news-audio-2.mp3",
        "audio_duration_seconds": 60,
        "mandal_name": "Sample Mandal",
        "published_at": "2026-11-17T11:00:00Z",
        "is_breaking": True,
        "reporter": {
            "name": "Sample Reporter"
        },
        "stats": {
            "views": 250
        }
    },
    {
        "id": "550e8400-e29b-41d4-a716-446655440003",
        "category": "Public Issues",
        "headline": "Officials discuss drinking water and sanitation concerns",
        "summary_60_words": (
            "Local representatives met residents to discuss drinking "
            "water supply, street lighting and sanitation concerns "
            "raised in recent community meetings. Officials said "
            "departments would inspect the reported locations and "
            "prepare a priority list for follow-up work. Residents "
            "requested clear timelines and regular updates on progress. "
            "The meeting concluded with a commitment to review "
            "unresolved complaints at the next mandal coordination "
            "meeting."
        ),
        "cover_image_url": "https://example.com/news-image-3.jpg",
        "blurhash": "",
        "audio_url": "https://example.com/news-audio-3.mp3",
        "audio_duration_seconds": 50,
        "mandal_name": "Sample Mandal",
        "published_at": "2026-11-17T12:00:00Z",
        "is_breaking": False,
        "reporter": {
            "name": "Sample Reporter"
        },
        "stats": {
            "views": 180
        }
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
