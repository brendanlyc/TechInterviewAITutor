from .prompt import router as prompt_routes
from .user import router as user_routes
from .progress import router as progress_routes
from .learning_path import router as learning_path_routes
from .level import router as level_routes

routes = [
    prompt_routes,
    user_routes,
    progress_routes,
    learning_path_routes,
    level_routes
]