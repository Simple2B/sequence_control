from time import time
from app.models import Location

__cached_locations = {}
__cached_timestamp = 0
CACHE_TIMEOUT = 5  # in seconds


def locations_for_project(project_id: int) -> list[Location]:
    global __cached_locations, __cached_timestamp
    if (
        project_id in __cached_locations
        and (__cached_timestamp - CACHE_TIMEOUT) < time()
    ):
        return __cached_locations[project_id]

    locations_ids = [
        loc.id
        for loc in Location.query.filter_by(deleted=False)
        if loc.level.building.project_id == project_id
    ]

    __cached_locations[project_id] = [
        location for location in Location.query.filter(Location.id.in_(locations_ids))
    ]
    __cached_timestamp = time()

    return __cached_locations[project_id]
