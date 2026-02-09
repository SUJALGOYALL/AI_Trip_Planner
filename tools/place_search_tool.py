import os
from typing import List
from langchain.tools import tool
from dotenv import load_dotenv

# optional imports (won't crash if unused)
try:
    from utils.place_info_search import GooglePlaceSearchTool, TavilyPlaceSearchTool
except ImportError:
    GooglePlaceSearchTool = None
    TavilyPlaceSearchTool = None


class PlaceSearchTool:
    def __init__(self):
        load_dotenv()

        self.google_api_key = os.getenv("GPLACES_API_KEY")
        self.tavily_api_key = os.getenv("TAVILY_API_KEY")

        self.google_places_search = None
        self.tavily_search = None

        self.place_search_tool_list = self._setup_tools()

    def _get_google_client(self):
        if self.google_api_key and self.google_places_search is None:
            self.google_places_search = GooglePlaceSearchTool(self.google_api_key)
        return self.google_places_search

    def _get_tavily_client(self):
        if self.tavily_api_key and self.tavily_search is None:
            self.tavily_search = TavilyPlaceSearchTool()
        return self.tavily_search

    def _static_fallback(self, place: str, category: str) -> str:
        """Final fallback when no APIs are available"""
        examples = {
            "attractions": "local landmarks, historical sites, markets, cultural spots",
            "restaurants": "popular local restaurants, street food areas, cafes",
            "activities": "sightseeing, local food exploration, cultural walks",
            "transportation": "local buses, taxis, auto-rickshaws, rental vehicles",
        }
        return (
            f"(Demo Mode) Since external APIs are not configured, here are common "
            f"{category} to explore in {place}: {examples.get(category)}."
        )

    def _setup_tools(self) -> List:

        @tool
        def search_attractions(place: str) -> str:
            """Search attractions of a place"""

            if self.google_api_key:
                try:
                    google = self._get_google_client()
                    return f"Attractions in {place}: {google.google_search_attractions(place)}"
                except Exception:
                    pass

            if self.tavily_api_key:
                try:
                    tavily = self._get_tavily_client()
                    return f"Attractions in {place}: {tavily.tavily_search_attractions(place)}"
                except Exception:
                    pass

            return self._static_fallback(place, "attractions")

        @tool
        def search_restaurants(place: str) -> str:
            """Search restaurants of a place"""

            if self.google_api_key:
                try:
                    google = self._get_google_client()
                    return f"Restaurants in {place}: {google.google_search_restaurants(place)}"
                except Exception:
                    pass

            if self.tavily_api_key:
                try:
                    tavily = self._get_tavily_client()
                    return f"Restaurants in {place}: {tavily.tavily_search_restaurants(place)}"
                except Exception:
                    pass

            return self._static_fallback(place, "restaurants")

        @tool
        def search_activities(place: str) -> str:
            """Search activities of a place"""

            if self.google_api_key:
                try:
                    google = self._get_google_client()
                    return f"Activities in {place}: {google.google_search_activity(place)}"
                except Exception:
                    pass

            if self.tavily_api_key:
                try:
                    tavily = self._get_tavily_client()
                    return f"Activities in {place}: {tavily.tavily_search_activity(place)}"
                except Exception:
                    pass

            return self._static_fallback(place, "activities")

        @tool
        def search_transportation(place: str) -> str:
            """Search transportation of a place"""

            if self.google_api_key:
                try:
                    google = self._get_google_client()
                    return f"Transportation in {place}: {google.google_search_transportation(place)}"
                except Exception:
                    pass

            if self.tavily_api_key:
                try:
                    tavily = self._get_tavily_client()
                    return f"Transportation in {place}: {tavily.tavily_search_transportation(place)}"
                except Exception:
                    pass

            return self._static_fallback(place, "transportation")

        return [
            search_attractions,
            search_restaurants,
            search_activities,
            search_transportation,
        ]

# import os
# from utils.place_info_search import GooglePlaceSearchTool, TavilyPlaceSearchTool
# from typing import List
# from langchain.tools import tool
# from dotenv import load_dotenv

# class PlaceSearchTool:
#     def __init__(self):
#         load_dotenv()
#         self.google_api_key = os.environ.get("GPLACES_API_KEY")
#         self.google_places_search = GooglePlaceSearchTool(self.google_api_key)
#         self.tavily_search = TavilyPlaceSearchTool()
#         self.place_search_tool_list = self._setup_tools()

#     def _setup_tools(self) -> List:
#         """Setup all tools for the place search tool"""
#         @tool
#         def search_attractions(place:str) -> str:
#             """Search attractions of a place"""
#             try:
#                 attraction_result = self.google_places_search.google_search_attractions(place)
#                 if attraction_result:
#                     return f"Following are the attractions of {place} as suggested by google: {attraction_result}"
#             except Exception as e:
#                 tavily_result = self.tavily_search.tavily_search_attractions(place)
#                 return f"Google cannot find the details due to {e}. \nFollowing are the attractions of {place}: {tavily_result}"  ## Fallback search using tavily in case google places fail
        
#         @tool
#         def search_restaurants(place:str) -> str:
#             """Search restaurants of a place"""
#             try:
#                 restaurants_result = self.google_places_search.google_search_restaurants(place)
#                 if restaurants_result:
#                     return f"Following are the restaurants of {place} as suggested by google: {restaurants_result}"
#             except Exception as e:
#                 tavily_result = self.tavily_search.tavily_search_restaurants(place)
#                 return f"Google cannot find the details due to {e}. \nFollowing are the restaurants of {place}: {tavily_result}"  ## Fallback search using tavily in case google places fail
        
#         @tool
#         def search_activities(place:str) -> str:
#             """Search activities of a place"""
#             try:
#                 restaurants_result = self.google_places_search.google_search_activity(place)
#                 if restaurants_result:
#                     return f"Following are the activities in and around {place} as suggested by google: {restaurants_result}"
#             except Exception as e:
#                 tavily_result = self.tavily_search.tavily_search_activity(place)
#                 return f"Google cannot find the details due to {e}. \nFollowing are the activities of {place}: {tavily_result}"  ## Fallback search using tavily in case google places fail
        
#         @tool
#         def search_transportation(place:str) -> str:
#             """Search transportation of a place"""
#             try:
#                 restaurants_result = self.google_places_search.google_search_transportation(place)
#                 if restaurants_result:
#                     return f"Following are the modes of transportation available in {place} as suggested by google: {restaurants_result}"
#             except Exception as e:
#                 tavily_result = self.tavily_search.tavily_search_transportation(place)
#                 return f"Google cannot find the details due to {e}. \nFollowing are the modes of transportation available in {place}: {tavily_result}"  ## Fallback search using tavily in case google places fail
        
#         return [search_attractions, search_restaurants, search_activities, search_transportation]