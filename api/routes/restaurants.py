from fastapi import APIRouter, HTTPException
from api.connection import create_connection

router = APIRouter()
r = create_connection()

@router.get("/v1/search/nearby")
def get_nearby_restaurants(lat: float, lng: float, radius: float = 5, unit: str = "mi"):
    try:
        # Find nearby restaurant IDs
        results = r.geosearch(
            'restaurant',
            longitude=lng,
            latitude=lat,
            radius=radius,
            unit=unit,
            withcoord=True,
            withdist=True,
            sort='ASC'
        )

        restaurants = []
        for result in results:
            node_id = result[0]
            distance = result[1]
            coords = result[2]

            # Get details from hash
            details = r.hgetall(f"restaurant:{node_id}")
            details['distance'] = distance
            details['id'] = node_id
            restaurants.append(details)

        return {"total": len(restaurants), "restaurants": restaurants}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/v1/restaurants/{node_id}")
def get_restaurant(node_id: str):
    details = r.hgetall(f"restaurant:{node_id}")
    if not details:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return details