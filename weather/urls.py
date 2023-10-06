from django.urls import path

from weather.views import CoolestDistrictView, PlaceToVisitView, SuggestFriendView

urlpatterns = [
    path("coolest_district/", CoolestDistrictView.as_view(), name="coolest_districts"),
    path("place_to_visit/", PlaceToVisitView.as_view(), name="place_to_visit"),
    path(
        "suggest_fiend/", SuggestFriendView.as_view(), name="suggest_fiend"
    ),  # host/api/suggest_fiend/?location=current_district_name&destination=destination_district_name&date=YYYY-MM-DD
]
