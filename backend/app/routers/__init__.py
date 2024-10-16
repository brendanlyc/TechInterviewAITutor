from .prompt import router as prompt_routes
from .user import router as user_routes
from .progress import router as progress_routes
from .learning_path import router as learning_path_routes
from .level import router as level_routes
from .content import router as content_routes
from .review_question import router as review_question_routes
from .auth import router as auth_routes
from .openai import router as openai_routes

routes = [
    prompt_routes,
    user_routes,
    progress_routes,
    learning_path_routes,
    level_routes,
    content_routes,
    review_question_routes,
    auth_routes,
    openai_routes
]