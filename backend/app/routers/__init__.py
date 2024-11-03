from .user import router as user_routes
from .learning_path import router as learning_path_routes
from .auth import router as auth_routes
from .diagnostic_test import router as diagnostic_test_routes
from .diagnostic_test_result import router as diagnostic_test_result_routes
from .ai_tutor import router as ai_tutor_routes

routes = [
    user_routes,
    learning_path_routes,
    auth_routes,
    diagnostic_test_routes,
    diagnostic_test_result_routes,
    ai_tutor_routes
]