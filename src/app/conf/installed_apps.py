# Application definition
INSTALLED_APPS = [
    'auth',
    'users',
    'shop',
    'health_check',
    'categories',
    'sellers',
    'seller_products',
    'sales',
    'languages',
    'geo_regions',
    'data_delivery_types',
    'product_data_types',
    'upload',

    'mptt',
    'data_generator',
    'djmoney',

    'corsheaders',
    'django_filters',
    'rest_framework',
    'rest_framework_simplejwt',

    'rangefilter',
    'django_admin_listfilter_dropdown',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
