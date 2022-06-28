from rest_framework.pagination import PageNumberPagination, CursorPagination
from urllib.parse import urlparse, parse_qs

'''
The default pagination class is assigned 
in settings.REST_FRAMEWORK.DEFAULT_PAGINATION_CLASS.
'''

class DefaultPageNumberPagination(PageNumberPagination):
    '''
    By default, DRF returns the full URL to the next page,
    but the frontend expects pages numbers instead of URLs.
    These methods override the default and return just the
    page number for the previous and next pages, respectively.
    '''

    def get_previous_link(self):
        if self.page.has_previous():
            return self.page.previous_page_number()

    def get_next_link(self):
        if self.page.has_next():
            return self.page.next_page_number()

class DefaultCursorPagination(CursorPagination):
    '''
    By default, DRF returns the full URL to the next page,
    but the frontend expects cursors instead of URLs.
    These methods override the default and return just the
    cursor for the previous and next pages, respectively.
    '''

    ordering = '-pk'
    
    # return the cursor instead of the link
    def get_previous_link(self):
        try:
            return parse_qs(urlparse(super().get_previous_link()).query)['cursor'][0]
        except:
            return None

    def get_next_link(self):
        try:
            return parse_qs(urlparse(super().get_next_link()).query)['cursor'][0]
        except:
            return None

    '''
    Additionally, it can be useful to have the cursor for the
    page of data in the response.
    
    1. `paginate_queryset` assigns the queryset to `self`.
    2. `decode_cursor` gets the encoded_cursor, using `self.queryset`
       from the previous step, and assigns to `self`.
    3. `get_paginated_response` then adds `cursor` to the response.
    '''

    def paginate_queryset(self, queryset, request, view=None):
        self.queryset = queryset
        return super().paginate_queryset(queryset, request, view=view)

    def decode_cursor(self, request):
        response = super().decode_cursor(request)
        self.encoded_cursor = request.query_params.get(self.cursor_query_param)
        return response

    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        response.data['cursor'] = self.encoded_cursor
        return response
