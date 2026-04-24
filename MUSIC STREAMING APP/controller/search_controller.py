



from service.search_service import SearchResponse, SearchService


class SearchController:
    def __init__(self, search_service: SearchService):
        self.search_service = search_service

    def search(self, query: str, type_str: str) -> SearchResponse:
        return self.search_service.search(query, type_str)