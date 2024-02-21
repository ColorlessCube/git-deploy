import os

from app import create_app
from cli import init_cli

# 获取应用配置&创建应用
app = create_app(os.getenv('APP_CONFIG', 'default'))

init_cli(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3668, debug=True)

__version__ = 'v1.6'
