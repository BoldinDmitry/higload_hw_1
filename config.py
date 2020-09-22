import pathlib

from solution.config_parser import parse_config

config = parse_config('/etc/httpd.conf')

HTTP_VERSION = 1.1
HTTP_ACCEPTABLE = ["HTTP/1.0", "HTTP/1.1"]

METHODS_ACCEPTABLE = ["GET", "HEAD"]

SERVER_NAME = "Dmitry Boldin's prefork server"

PROJECT_ROOT = pathlib.Path(config.get("document_root", pathlib.Path(__file__).parent.absolute()))
MEDIA_FOLDER_NAME = "httptest"
MEDIA_ROOT = PROJECT_ROOT.joinpath(MEDIA_FOLDER_NAME)

ADDRESS = "localhost"
PORT = 80

MAX_CONNECTIONS = 5
CPU_LIMIT = int(config.get("cpu_limit", 4))
