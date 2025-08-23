"""Route package: expose blueprints to the app factory."""
# from modules import forum as forum_module

from .auth import bp as auth_bp
from .home import bp as home_bp
from .user import bp as user_bp
from .misc import bp as misc_bp
from .forum import bp as forum_bp

blueprints = [
    auth_bp,
    forum_bp,
    home_bp,
    user_bp,
    misc_bp,
]
