# flake8: noqa F401
from .auth import auth_blueprint
from .main import main_blueprint
from .user.user import user_blueprint
from .define import define_blueprint
from .user.project_manager import project_manager_blueprint
from .user.viewer import viewer_blueprint
