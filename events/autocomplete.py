import json
from dal import autocomplete
from dal.views import ViewMixin
from django_countries import countries
from common.models import Sector, Motive
from dal.autocomplete import Select2ListView
from users.views import UserCanViewDataMixin

class SectorAutocomplete(UserCanViewDataMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Sector.objects.none()

        qs = Sector.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


class MotiveAutocomplete(UserCanViewDataMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Motive.objects.none()

        qs = Motive.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


class CountryAutocompleteFromList(UserCanViewDataMixin, Select2ListView):
    def get_list(self):
        contries_dict = countries.countries
        countries_list = list()
        for key, value in contries_dict.items():
            countries_list.append(str(value))

        return contries_dict

    def autocomplete_results(self, results):
        """Return list of strings that match the autocomplete query."""

        return [dict(id=str(key), text=str(value)) for key, value in results.items()
                if self.q.lower() in value.lower()]


    def results(self, results):
        """Return the result dictionary."""

        if isinstance(results, dict):
            return [dict(id=str(key), text=str(value)) for key, value in results.items()]

        else:
            return [x for x in results]


    def get(self, request, *args, **kwargs):
        """Return option list json response."""
        results = self.get_list()
        create_option = []
        if self.q:
            results = self.autocomplete_results(results)

        return http.HttpResponse(json.dumps({
            'results': self.results(results),
            'pagination': {'more': False}
        }), content_type='application/json')



