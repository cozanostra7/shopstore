from store.models import Collection,Product
from rest_framework import status
from model_bakery import baker
import pytest


@pytest.fixture
def create_collection(api_client):
    def do_create_collection(collection):
        return api_client.post('/collections/',collection)
    return do_create_collection

#декоратор, который после выполнения тестов вернет базу в исходное состояние
@pytest.mark.django_db

class TestCreateCollection:
    def test_if_user_is_anonymous_return_401(self,create_collection):
        response=create_collection({'title': 'Тестовая категория'})
        assert response.status_code==status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_return_403(self,authenticate,create_collection):
        authenticate()
        response=create_collection({'title':'Тестовая категория'})
        assert response.status_code==status.HTTP_403_FORBIDDEN


    def test_if_data_is_invalid_return_400(self,authenticate,create_collection):
        authenticate(is_staff=True)
        response=create_collection({'title':''})
        assert response.status_code==status.HTTP_400_BAD_REQUEST

    def test_if_data_valid_return_201(self,authenticate,create_collection):
        authenticate(is_staff=True)
        response=create_collection({'title':'Тестовая категория'})
        assert response.status_code==status.HTTP_201_CREATED
        assert response.data['id']>0

@pytest.mark.django_db
class TestRetrieveCollection:
    def test_if_collection_exists_return_200(self,api_client):
        collection=baker.make(Collection)#Создает тестовую категорию не трогая базу
        response=api_client.get(f'/collections/{collection.id}/')
        assert response.status_code==status.HTTP_200_OK