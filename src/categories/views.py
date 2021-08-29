from django.core.exceptions import ImproperlyConfigured
from django.db.models import QuerySet
from django.http import Http404, HttpResponse
from django.views import View
from django.views.generic import ListView

from categories.models import Category


class CategoryListView(ListView):
    model = Category
    filters = ['parent_id', 'name']

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()

        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, 'exists'):
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list
            if is_empty:
                raise Http404(_('Empty list and “%(class_name)s.allow_empty” is False.') % {
                    'class_name': self.__class__.__name__,
                })
        context = self.get_context_data()

        #todo: replace by serializing context
        return self.render_to_response(context)

    def get_queryset(self):
        """
        Return the list of items for this view.

        The return value must be an iterable and may be an instance of
        `QuerySet` in which case `QuerySet` specific behavior will be enabled.
        """
        if self.queryset is not None:
            queryset = self.queryset
            if isinstance(queryset, QuerySet):
                queryset = queryset.all()
        elif self.model is not None:
            queryset = self.model._default_manager.all()
        else:
            raise ImproperlyConfigured(
                "%(cls)s is missing a QuerySet. Define "
                "%(cls)s.model, %(cls)s.queryset, or override "
                "%(cls)s.get_queryset()." % {
                    'cls': self.__class__.__name__
                }
            )

        queryset = self.filter_queryset(queryset)

        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)

        return queryset

    def filter_queryset(self, queryset):
        filters_data = {}

        if self.filters:

            for _filter in self.filters:
                value = self.request.GET.get(_filter)
                if value:
                    filters_data[_filter] = self.request.GET.get(_filter)

            if filters_data:
                return queryset.filter(
                    **filters_data
                )

        return queryset