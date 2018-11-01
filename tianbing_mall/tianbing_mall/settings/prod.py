"""
Django settings for tianbing_mall project.

Generated by 'django-admin startproject' using Django 1.11.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""
import datetime
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path保存了python解释器的导包路径
sys.path.insert(0, os.path.join(BASE_DIR, "apps"))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6@z(i$c69u#%g-s=(^-n4pr+8bfs+wle9wt8i&4k_tspr%f=d_'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = False  # 修改

# ALLOWED_HOSTS = ["api.tianbing.site", "127.0.0.1", "localhost", "www.tianbing.site"]
ALLOWED_HOSTS = ["api.meiduo.site", "127.0.0.1", "localhost", "www.meiduo.site"]  # 添加最后一个


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',  # 注册django-cors-headers跨域
    'ckeditor',  # 富文本编辑器
    'ckeditor_uploader',  # 富文本编辑器上传图片模块
    'django_crontab',  # 定时任务
    'haystack',  # 注册haystack,用于调用对接Elasticsearch搜索引擎

    'xadmin',  # 注册xadmin
    'crispy_forms',  # xadmin依赖
    'reversion',  # xadmin依赖

    'users.apps.UsersConfig',
    'verifications.apps.VerificationsConfig',
    'oauth.apps.OauthConfig',  # 注册qq登录应用
    'areas.apps.AreasConfig',  # 收货地址应用
    'goods.apps.GoodsConfig',
    'contents.apps.ContentsConfig',
    'orders.apps.OrdersConfig',  # 订单
    'payment.apps.PaymentConfig',  # 支付

]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # 专门解决跨域请求问题
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tianbing_mall.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'tianbing_mall.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        # 修改数据库配置：
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',  # 数据库主机
        'PORT': 3306,  # 数据库端口
        'USER': 'tb',  # 数据库用户名
        'PASSWORD': 'tb',  # 数据库用户密码
        'NAME': 'Tianbing_Mall'  # 数据库名字
    },
    'slave': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',
        'PORT': 8306,
        'USER': 'root',
        'PASSWORD': 'mysql',
        'NAME': 'Tianbing_Mall'
    }
}

# django-redis配置
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "session": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "verify_codes": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    # 商品浏览历史记录
    "history": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/3",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "cart": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/4",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
}
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "session"


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

# 配置日志
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(os.path.dirname(BASE_DIR), "logs/tianbing_mall.log"),  # 日志文件的位置
            'maxBytes': 300 * 1024 * 1024,
            'backupCount': 10,
            'formatter': 'verbose'
        },
    },

    'loggers': {
        'django': {  # 定义了一个名为django的日志器
            'handlers': ['console', 'file'],
            'propagate': True,
        },
    }
}

# rest_framework配置
REST_FRAMEWORK = {
    # 异常处理
    'EXCEPTION_HANDLER': 'tianbing_mall.utils.exceptions.exception_handler',
    # 配置认证
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 使用JWT认证
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    # 配置全局默认分页
    "DEFAULT_PAGINATION_CLASS": "tianbing_mall.utils.pagination.StandardResultsSetPagination",

}

# JWT有效期
JWT_AUTH = {
    # delta:时间间隔
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),

    'JWT_RESPONSE_PAYLOAD_HANDLER': 'users.utils.jwt_response_payload_handler',

}

# 配置使用自定义的认证后端
AUTHENTICATION_BACKENDS = [
    'users.utils.UsernameMobileAuthBackend',
]

# 配置用户模型
AUTH_USER_MODEL = 'users.User'

# CORS跨域白名单:凡是出现在白名单中的域名，都可以访问后端接口
CORS_ORIGIN_WHITELIST = (
    # '127.0.0.1:8080',
    # 'localhost:8080',
    # 'www.tianbing.site:8080',
    # 'api.tianbing.site:8000',

    '127.0.0.1:8080',
    'localhost:8080',
    'www.meiduo.site:8080',
    'www.meiduo.site',  # 添加
    'api.meiduo.site:8000',
)
# 跨域允许携带cookie
CORS_ALLOW_CREDENTIALS = True

# QQ登录参数
QQ_CLIENT_ID = '101474184'
QQ_CLIENT_SECRET = 'c6ce949e04e12ecc909ae6a8b09b637c'
QQ_REDIRECT_URI = 'http://www.meiduo.site:8080/oauth_callback.html'
QQ_STATE = '/'

# 配置邮箱信息
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.163.com'
EMAIL_PORT = 25
# 发送邮件的邮箱
EMAIL_HOST_USER = 'tianbing_admin@163.com'
# 在邮箱中设置的客户端授权密码
EMAIL_HOST_PASSWORD = 'tianbing163'
# 收件人看到的发件人
EMAIL_FROM = '天冰商城<tianbing_admin@163.com>'

# DRF -extensions缓存扩展
REST_FRAMEWORK_EXTENSIONS = {
    # 缓存时间:设为1小时
    'DEFAULT_CACHE_RESPONSE_TIMEOUT': 60 * 60,
    # 缓存存储
    'DEFAULT_USE_CACHE': 'default',
}

# django文件存储
DEFAULT_FILE_STORAGE = 'tianbing_mall.utils.fastdfs.fdfs_storage.FastDFSStorage'

# FastDFS配置
FDFS_URL = 'http://image.meiduo.site:8888/'
FDFS_CLIENT_CONF = os.path.join(BASE_DIR, 'utils/fastdfs/client.conf')

# 富文本编辑器ckeditor配置
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',  # 工具条功能
        'height': 300,  # 编辑器高度
        # 'width': 300,  # 编辑器宽
    },
}
CKEDITOR_UPLOAD_PATH = ''  # 上传图片保存路径，使用了FastDFS，所以此处设为''

# 配置生成的静态html文件保存目录
GENERATED_STATIC_HTML_FILES_DIR = os.path.join(os.path.dirname(os.path.dirname(BASE_DIR)), 'front_end_pc')

# 配置crontab定时任务
CRONJOBS = [
    # 每5分钟执行一次生成主页静态文件;
    # 3个参数(任务时间, 任务函数名, 任务日志保存位置)
    # 'contents.crons.generate_static_index_html', '>> /home/python/Desktop//logs/crontab.log')
    ('*/5 * * * *', 'contents.crons.generate_static_index_html', '>> ' + os.path.join(os.path.dirname(BASE_DIR), "logs/crontab.log"))
]
'''
注意:1,* * * * * *对应
    2,>> 与 >的区别:前者追加,后者覆盖
'''

# 解决crontab中文问题:让操作系统执行crontab之前加上中文编码前缀
CRONTAB_COMMAND_PREFIX = 'LANG_ALL=zh_cn.UTF-8'

# 配置Haystack使用的搜索引擎后端:即连接elasticsearch
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        # 此处为elasticsearch运行的服务器ip地址，端口号固定为9200
        'URL': 'http://192.168.31.128:9200/',
        # 指定elasticsearch建立的索引库的名称
        'INDEX_NAME': 'tianbing',
    },
}
# 当添加、修改、删除数据时，自动生成索引
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

# 支付宝配置
ALIPAY_APPID = 2016092200568771
ALIPAY_DEBUG = True
ALIPAY_URL = "https://openapi.alipaydev.com/gateway.do"

# 配置读写分离分发类
DATABASE_ROUTERS = ['tianbing_mall.utils.db_router.MasterSlaveDBRouter']

# 收集django的静态文件的保存目录(django线上模式不在提供admin站点的样式)
STATIC_ROOT = os.path.join(os.path.dirname(os.path.dirname(BASE_DIR)), 'front_end_pc/static')












