from project import create_app
from project.config import DeploymentConfig


application = create_app(DeploymentConfig)


