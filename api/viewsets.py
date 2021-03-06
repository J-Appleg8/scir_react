from rest_framework import viewsets, filters
from zen_queries.rest_framework import QueriesDisabledViewMixin


class InvalidProjectionError(Exception):
    pass


class InvalidFilterError(Exception):
    pass


class ProjectionsAndFilters(viewsets.ModelViewSet, QueriesDisabledViewMixin):
    filter_backends = [filters.OrderingFilter]
    ordering = ["id"]

    projection = None
    projections = {}
    filters = {}
    _default_filters = [
        "page",
    ]

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "GET":

            if self.request.query_params:

                self.projection = self.request.query_params.get("projection", None)

                if self.projection:

                    # throw an error if an invalid projection is requested
                    if self.projection and self.projection not in self.serializers.for_.keys():
                        raise InvalidProjectionError(f'Invalid projection: "{self.projection}"')

                    return self.serializers.for_[self.projection]

        else:
            method_serializer = self.serializers.for_.get(self.request.method)
            if method_serializer:
                return method_serializer

        return super().get_serializer_class()

    def get_queryset(self):
        q = super().get_queryset()

        if self.request.query_params:
            parameters = dict(self.request.query_params.items())

            # for paginated queries:
            parameters.pop("cursor", None)

            # for ordered queries:
            ordering = parameters.pop("ordering", None)

            # # throw an error if an invalid projection is requested
            projection = parameters.pop("projection", None)

            # coming from request.query_params
            if projection:
                projection_serializer = self.serializers.for_[projection]
                if projection_serializer:
                    if hasattr(projection_serializer, "chain_queryset"):
                        q = projection_serializer.chain_queryset(q, self.request)

            # throw an error if an invalid filter is specified
            filters = parameters.keys()
            for filter in filters:
                if filter not in [*self._default_filters, *self.filters.keys()]:
                    raise InvalidFilterError(f'Invalid filter: "{filter}"')

            # dynamically build the list of filters on the queryset
            if filters:
                for filter in filters:
                    q = self.filters[filter](q, self.request.query_params.get(filter), self.request)

        return q
