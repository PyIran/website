from project import create_app
from project.config import DevelopmentConfig

application = create_app(DevelopmentConfig)

