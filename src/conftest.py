import pytest
import uuid
from mixer.backend.django import mixer

from categories.models import Category, RecommendedFor
from data_delivery_types.models import DataDeliveryType
from geo_regions.models import GeoRegion
from languages.models import Language
from product_data_types.models import DataType, DataFormat
from users.models import User

mixer.register(User,
               uuid=lambda: uuid.uuid4())


@pytest.fixture
def superuser():
    return mixer.blend(User,
                       username='superuser@gmail.com',
                       is_superuser=True)


@pytest.fixture
def recommended_for():
    recommended_for_1 = mixer.blend(RecommendedFor,
                                    name='recommended_for->category-1')
    recommended_for_2 = mixer.blend(RecommendedFor,
                                    name='recommended_for->category-2')
    return recommended_for_1, recommended_for_2


@pytest.fixture
def categories(recommended_for):
    category_1 = mixer.blend(Category,
                             name='category-1',
                             logo_url='',
                             recommended_for=recommended_for[0])

    category_2 = mixer.blend(Category,
                             name='category-2',
                             logo_url='',
                             recommended_for=recommended_for[1])
    return category_1, category_2


@pytest.fixture
def geo_regions():
    geo_region_1 = mixer.blend(GeoRegion,
                               name='geo-region-1',
                               paent=None)
    geo_region_2 = mixer.blend(GeoRegion,
                               name='geo-region-2',
                               parent=None)
    mixer.blend(GeoRegion,
                name='geo-region-3-children-of-GR-2',
                parent=geo_region_2)
    return geo_region_1, geo_region_2


@pytest.fixture
def languages():
    language_1 = mixer.blend(Language,
                             name_en='language_1',
                             name_native='language-1-native-name')
    language_2 = mixer.blend(Language,
                             name_en='language_2',
                             name_native='language-2-native-name')
    return language_1, language_2


@pytest.fixture
def data_types():
    data_type_1 = mixer.blend(DataType,
                              name='data_type_1')
    data_type_2 = mixer.blend(DataType,
                              name='data_type_2')
    return data_type_1, data_type_2


@pytest.fixture
def data_formats(data_types):
    data_format_1 = mixer.blend(DataFormat,
                                data_type_id=data_types[0],
                                name='data_format_1')
    data_format_2 = mixer.blend(DataFormat,
                                data_type_id=data_types[1],
                                name='data_format_2')
    return data_format_1, data_format_2


@pytest.fixture
def data_delivery_types():
    data_delivery_type_1 = mixer.blend(DataDeliveryType,
                                       name='data_delivery_type_1')
    data_delivery_type_2 = mixer.blend(DataDeliveryType,
                                       name='data_delivery_type_2')
    return data_delivery_type_1, data_delivery_type_2
