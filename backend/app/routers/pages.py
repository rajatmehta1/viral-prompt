"""
Template rendering routes for all pages
"""
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")


# Sample data for templates
SAMPLE_CONTENT = [
    {
        "id": 1,
        "title": "Majestic Mountain Sunset",
        "description": "Breathtaking view of sunset over the peaks",
        "image": "https://images.unsplash.com/photo-1682687220742-aba13b6e50ba?w=400&h=600&fit=crop",
        "type": "images",
        "author": "@naturelover",
        "author_avatar": "https://i.pravatar.cc/40?img=1",
        "likes": "2.4k"
    },
    {
        "id": 2,
        "title": "Dance Challenge Viral Hit",
        "description": "This dance move is breaking the internet! 🔥",
        "image": None,
        "gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        "type": "reels",
        "platform": "tiktok",
        "duration": "0:45",
        "author": "@danceking",
        "author_avatar": "https://i.pravatar.cc/40?img=2",
        "views": "1.2M"
    },
    {
        "id": 3,
        "title": "Cyberpunk Dreams",
        "description": "AI-generated futuristic cityscape",
        "image": "https://images.unsplash.com/photo-1686191128892-3b37add4b844?w=400&h=400&fit=crop",
        "type": "ai",
        "author": "@ai_artist",
        "author_avatar": "https://i.pravatar.cc/40?img=3",
        "likes": "5.7k"
    },
    {
        "id": 4,
        "title": "Turquoise Paradise",
        "description": "Crystal clear ocean waves at sunrise",
        "image": "https://images.unsplash.com/photo-1518837695005-2083093ee35b?w=400&h=500&fit=crop",
        "type": "images",
        "author": "@oceanvibes",
        "author_avatar": "https://i.pravatar.cc/40?img=4",
        "likes": "8.9k"
    },
]

SAMPLE_CATEGORIES = [
    {"name": "AI Art", "icon": "bi-stars", "count": "12.4K", "image": "https://images.unsplash.com/photo-1686191128892-3b37add4b844?w=400"},
    {"name": "Nature", "icon": "bi-tree", "count": "8.9K", "image": "https://images.unsplash.com/photo-1682687220742-aba13b6e50ba?w=400"},
    {"name": "Travel", "icon": "bi-airplane", "count": "15.2K", "image": "https://images.unsplash.com/photo-1493246507139-91e8fad9978e?w=400"},
    {"name": "Ocean", "icon": "bi-water", "count": "6.7K", "image": "https://images.unsplash.com/photo-1518837695005-2083093ee35b?w=400"},
]

SAMPLE_PROMPTS = [
    {
        "id": 1,
        "title": "Cinematic Portrait Photography",
        "description": "Create stunning portrait photos with dramatic lighting",
        "category": "Photography",
        "type": "image",
        "use_count": 1234,
        "like_count": 567,
        "author": "@portrait_master"
    },
    {
        "id": 2,
        "title": "Viral TikTok Hook",
        "description": "Generate attention-grabbing video hooks",
        "category": "Video",
        "type": "video",
        "use_count": 2345,
        "like_count": 890,
        "author": "@viral_creator"
    },
]


@router.get("/")
async def home(request: Request):
    """Render the home page"""
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "content": SAMPLE_CONTENT,
            "page_title": "Viral Prompt | Discover Amazing Content"
        }
    )


@router.get("/explore")
async def explore(request: Request):
    """Render the explore page"""
    return templates.TemplateResponse(
        request=request,
        name="explore.html",
        context={
            "categories": SAMPLE_CATEGORIES,
            "page_title": "Explore | Viral Prompt"
        }
    )


@router.get("/trending")
async def trending(request: Request):
    """Render the trending page"""
    return templates.TemplateResponse(
        request=request,
        name="trending.html",
        context={
            "content": SAMPLE_CONTENT,
            "page_title": "Trending | Viral Prompt"
        }
    )


@router.get("/prompt-library")
async def prompt_library(request: Request):
    """Render the prompt library page"""
    return templates.TemplateResponse(
        request=request,
        name="prompt-library.html",
        context={
            "prompts": SAMPLE_PROMPTS,
            "page_title": "Prompt Library | Viral Prompt"
        }
    )


@router.get("/dashboard")
async def dashboard(request: Request):
    """Render the user dashboard"""
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "page_title": "Dashboard | Viral Prompt"
        }
    )


@router.get("/profile")
async def profile(request: Request):
    """Render the user profile page"""
    return templates.TemplateResponse(
        request=request,
        name="profile.html",
        context={
            "page_title": "Profile | Viral Prompt"
        }
    )


@router.get("/settings")
async def settings(request: Request):
    """Render the settings page"""
    return templates.TemplateResponse(
        request=request,
        name="settings.html",
        context={
            "page_title": "Settings | Viral Prompt"
        }
    )


@router.get("/collections")
async def collections(request: Request):
    """Render the collections page"""
    return templates.TemplateResponse(
        request=request,
        name="collections.html",
        context={
            "page_title": "Collections | Viral Prompt"
        }
    )


@router.get("/signin")
async def signin(request: Request):
    """Render the sign in page"""
    return templates.TemplateResponse(
        request=request,
        name="signin.html",
        context={
            "page_title": "Sign In | Viral Prompt"
        }
    )


@router.get("/analytics")
async def analytics(request: Request):
    """Render the analytics page"""
    return templates.TemplateResponse(
        request=request,
        name="analytics.html",
        context={
            "page_title": "Analytics | Viral Prompt"
        }
    )


# AI Tools Pages
@router.get("/ai-books")
async def ai_books(request: Request):
    """Render the AI Books page"""
    return templates.TemplateResponse(
        request=request,
        name="ai-books.html",
        context={
            "page_title": "AI Books | Viral Prompt"
        }
    )


@router.get("/ai-music")
async def ai_music(request: Request):
    """Render the AI Music page"""
    return templates.TemplateResponse(
        request=request,
        name="ai-music.html",
        context={
            "page_title": "AI Music | Viral Prompt"
        }
    )


@router.get("/ai-video-generator")
async def ai_video_generator(request: Request):
    """Render the AI Video Generator page"""
    return templates.TemplateResponse(
        request=request,
        name="ai-video-generator.html",
        context={
            "page_title": "AI Video Generator | Viral Prompt"
        }
    )


@router.get("/caption-generator")
async def caption_generator(request: Request):
    """Render the Caption Generator page"""
    return templates.TemplateResponse(
        request=request,
        name="caption-generator.html",
        context={
            "page_title": "Caption Generator | Viral Prompt"
        }
    )


@router.get("/script-writer")
async def script_writer(request: Request):
    """Render the Script Writer page"""
    return templates.TemplateResponse(
        request=request,
        name="script-writer.html",
        context={
            "page_title": "Script Writer | Viral Prompt"
        }
    )


@router.get("/reel-creator")
async def reel_creator(request: Request):
    """Render the Reel Creator page"""
    return templates.TemplateResponse(
        request=request,
        name="reel-creator.html",
        context={
            "page_title": "AI Reel Creator | Viral Prompt"
        }
    )
