from .models import CategoryName, Categories
from .serializers import CategorySerializer
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.db import IntegrityError


class CategoriesAPI(APIView):
    def post(self, request):
        response = request.data
        try:
            category_object = request.data.get('name')
            parent_category = CategoryName(name=category_object)
            parent_category.save()
            children = request.data.get('children')
            if children:
                post_children(children, parent_category)
        except IntegrityError as e:
            response = f"{e}: category already exists!"
        return Response(data=response)


class CategoriesAPIView(APIView):
    def get(self, request, id):
        global response_parents
        response_parents = []
        category = get_object_or_404(CategoryName, pk=id)
        if category:
            response_childrens = retrieve_children(category)
            response_parents = retrieve_parents(category)
            response_siblings = retrieve_siblings(category)

            category_serializer = CategorySerializer(category)
            category_dict = category_serializer.data

            category_dict['parents'] = response_parents
            category_dict['children'] = response_childrens
            category_dict['siblings'] = response_siblings
            return Response(data=category_dict)
        else:
            return Response(data="No such category!")

def retrieve_parents(category):
    parents = Categories.objects.filter(children=category)
    for parent in parents:
        if parent:
            category_serializer = CategorySerializer(parent.category)
            if category_serializer.data not in response_parents:
                response_parents.append(category_serializer.data)
            retrieve_parents(parent.category)
    return response_parents

def retrieve_children(category):
    response_children = []
    parent = Categories.objects.get(category=category)
    children = parent.children.all()
    for child in children:
        if child:
            category_serializer = CategorySerializer(child)
            response_children.append(category_serializer.data)
    return response_children

def retrieve_siblings(category):
    response_siblings = []
    try:
        parent = Categories.objects.get(children=category)
        children = parent.children.all()
        for child in children:
            if child.id is not category.id:
                category_serializer = CategorySerializer(child)
                response_siblings.append(category_serializer.data)
        return response_siblings
    except Categories.DoesNotExist:
        return response_siblings

def post_children(children, parent_category):
    for category in children:
        if 'name' in category:
            try:
                category_obj_name = category['name']
                parent_category_new = CategoryName(name=category_obj_name)
                parent_category_new.save()
                parent_category.category_obj.children.add(parent_category_new)
            except IntegrityError as e:
                response = f"{e}:category with this name already exists"
                return Response(data=response)
        if 'children' in category:
            children = category['children']
            post_children(children, parent_category_new)
