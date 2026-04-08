from rest_framework.decorators import api_view
from rest_framework.response import Response
from bson import ObjectId
from datetime import datetime
from .mongo import menu_collection
from .serializers import MenuSerializer

# helper
def serialize_menu(menu):
    menu["id"] = str(menu["_id"])
    del menu["_id"]
    return menu


# ✅ CREATE
@api_view(['POST'])
def create_menu(request):
    serializer = MenuSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data
        data["created_at"] = datetime.utcnow()

        result = menu_collection.insert_one(data)
        return Response({
            "message": "Menu created",
            "id": str(result.inserted_id)
        })
    return Response(serializer.errors, status=400)


# ✅ GET ALL + SEARCH + FILTER
@api_view(['GET'])
def get_menus(request):
    query = {}

    restaurant = request.GET.get('restaurant')
    category = request.GET.get('category')
    available = request.GET.get('available')

    if restaurant:
        query["restaurant_name"] = {"$regex": restaurant, "$options": "i"}

    if category:
        query["category"] = category

    if available is not None:
        query["is_available"] = available.lower() == "true"

    menus = menu_collection.find(query)
    return Response([serialize_menu(menu) for menu in menus])


# ✅ GET BY ID
@api_view(['GET'])
def get_menu_by_id(request, id):
    try:
        menu = menu_collection.find_one({"_id": ObjectId(id)})
        if not menu:
            return Response({"error": "Not found"}, status=404)
        return Response(serialize_menu(menu))
    except:
        return Response({"error": "Invalid ID"}, status=400)


# ✅ UPDATE
@api_view(['PUT'])
def update_menu(request, id):
    serializer = MenuSerializer(data=request.data)
    if serializer.is_valid():
        result = menu_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": serializer.validated_data}
        )

        if result.matched_count == 0:
            return Response({"error": "Not found"}, status=404)

        return Response({"message": "Menu updated"})
    return Response(serializer.errors, status=400)


# ✅ DELETE
@api_view(['DELETE'])
def delete_menu(request, id):
    result = menu_collection.delete_one({"_id": ObjectId(id)})

    if result.deleted_count == 0:
        return Response({"error": "Not found"}, status=404)

    return Response({"message": "Menu deleted"})