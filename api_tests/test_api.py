import pytest
import requests

@pytest.fixture
def api_client():
    class ApiClient:
        base_url = "https://agate-gisogd.ivanovoobl.ru"
        
        def get_map_config(self, project):
            return requests.get(f"{self.base_url}/api/mapconfig/{project}")
            
        def get_sections(self, project):
            return requests.get(f"{self.base_url}/api/gisogdSections/{project}")
            
        def search_zu(self, project, query):
            return requests.get(f"{self.base_url}/api/v1/zusearch/{project}?search={query}")
            
    return ApiClient()

class TestMapConfig:
    def test_map_config_success(self, api_client):
        """Проверка получения конфигурации карты"""
        response = api_client.get_map_config("agate_ivanovoobl")
        assert response.status_code == 200
        data = response.json()
        assert "mapBounds" in data
        assert "backgroundLayers" in data
        assert "boundsGeometryJson" in data

class TestSections:
    def test_sections_count(self, api_client):
        """Проверка количества разделов реестра"""
        response = api_client.get_sections("agate_ivanovoobl")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 11 # В ГИСОГД Ивановской области 10 разделов

class TestZuSearch:
    def test_search_by_cadastral_prefix(self, api_client):
        """Поиск земельного участка по префиксу кадастрового номера"""
        response = api_client.search_zu("agate_ivanovoobl", "37")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
