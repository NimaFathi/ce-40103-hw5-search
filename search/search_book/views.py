from collections import defaultdict

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from _helpers.sql import establish_connection, execute_query, close_connection


@api_view(['GET', ])
def search_view(request):
    data = defaultdict(int)
    search_type = request.data.get('type', None)
    if search_type not in ['category', 'title']:
        return Response(data='invalid search type', status=status.HTTP_400_BAD_REQUEST)
    if search_type == 'title':
        query = find_icontains_query(text=request.data.get('text', None))
        if query is None:
            return Response(data='no match', status=status.HTTP_200_OK)
        for q in query:
            data[q[0]] = q[1:]
        return Response(data=data, status=status.HTTP_200_OK)
    category = request.data.get('category', None)
    if category not in ['textbook', 'historical', 'scientific', 'novel']:
        return Response(data='category incorrect', status=status.HTTP_400_BAD_REQUEST)
    query = find_category_query(category=category)
    if query is None:
        return Response(data='no match', status=status.HTTP_200_OK)
    for q in query:
        data[q[0]] = q[1:]
    return Response(data=data, status=status.HTTP_200_OK)

def find_icontains_query(text):
    if text is None:
        return None
    command = "SELECT * FROM book_management_book WHERE title LIKE %s escape '' "
    connection = establish_connection()
    query = execute_query(connection, command, ["%" + text + "%"])
    close_connection(connection)
    return query

def find_category_query(category):
    if category is None:
        return None
    command = "SELECT * FROM book_management_book WHERE category = %s"
    connection = establish_connection()
    query = execute_query(connection, command, [category])
    close_connection(connection)
    return query