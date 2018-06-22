import sqlite3

from registration import register
from resource import Resource
from location.models import Location, Country, State


class CityResource(Resource):

    allowed_methods = ('filter',)

    def filter(self, filter_args, top=0, *args, **kwargs):

        cx = sqlite3.connect("test_city.sqlite")
        cu = cx.cursor()
        cu.execute("select * from tbl_city")
        city_tups = cu.fetchall()

        objects = []
        number = 0
        for i, city_tup in enumerate(city_tups):
            state_name = city_tup[5]
            city_name = city_tup[3]
            city_cn_name = city_tup[6]
            state = State.objects.filter(cn_name=state_name).first()
            if state and city_name:
                context_object = {}
                number = number + 1
                context_object['pk'] = number
                context_object['model'] = 'location.city'
                context_object['fields'] = {}
                context_object['fields']['state'] = state.id
                context_object['fields']['name'] = city_name
                context_object['fields']['cn_name'] = city_cn_name
                objects.append(context_object)

        return {
            'status_code': 200,
            'data': objects
        }


class StateResource(Resource):

    allowed_methods = ('filter',)

    def filter(self, filter_args, top=0, *args, **kwargs):

        cx = sqlite3.connect("test_city.sqlite")
        cu = cx.cursor()
        cu.execute("select * from tbl_city")
        state_tups = cu.fetchall()

        objects = []
        states = State.objects.all()

        for i, state in enumerate(states):
            context_object = {}
            context_object['pk'] = i + 1
            context_object['name'] = state.name
            context_object['code'] = state.code
            for state_tup in state_tups:
                if state.name == state_tup[2]:
                    context_object['cn_name'] = state_tup[5]
                    break
                else:
                    context_object['cn_name'] = None

            objects.append(context_object)

        return {
            'status_code': 200,
            'data': objects
        }


class CountryResource(Resource):

    allowed_methods = ('filter',)

    def filter(self, filter_args, top=0, *args, **kwargs):

        cx = sqlite3.connect("test_city.sqlite")
        cu = cx.cursor()
        cu.execute("select * from tbl_city")
        country_tups = cu.fetchall()

        objects = []
        countries = Country.objects.all()

        for i, country in enumerate(countries):
            context_object = {}
            context_object['pk'] = i + 1
            context_object['name'] = country.name
            context_object['code'] = country.code
            for country_tup in country_tups:
                if country.name == country_tup[1]:
                    context_object['cn_name'] = country_tup[4]
                    break
                else:
                    context_object['cn_name'] = None

            objects.append(context_object)

        return {
            'status_code': 200,
            'data': objects
        }


class LocationResource(Resource):

    allowed_methods = ('filter',)

    def filter(self, filter_args, top=0, *args, **kwargs):

        cx = sqlite3.connect("test_city.sqlite")
        cu = cx.cursor()
        cu.execute("select * from tbl_city")
        location_tups = cu.fetchall()

        objects = []
        locations = Location.objects.all()

        for i, country in enumerate(locations):
            context_object = {}
            context_object['pk'] = i + 1
            context_object['name'] = country.name
            for location_tup in location_tups:
                if country.name == location_tup[1]:
                    context_object['cn_name'] = location_tup[4]
                    break
                else:
                    context_object['cn_name'] = None

            objects.append(context_object)

        return {
            'status_code': 200,
            'data': objects
        }


class HKResource(Resource):

    allowed_methods = ('filter',)

    def filter(self, filter_args, top=0, *args, **kwargs):

        cx = sqlite3.connect("test_city.sqlite")
        cu = cx.cursor()
        cu.execute("select * from tbl_city")
        country_tups = cu.fetchall()

        objects = []

        dot = 3335
        area = ['MO', 'TW', 'HK']
        i = 1
        prev_code = ''

        for country_tup in country_tups:
            code = country_tup[0]
            if prev_code != code:
                prev_code = code
                i = 1
            code_id = "%02d" % i
            if code in area:
                code_id = Country.objects.filter(code=code).first().pk
                context_object = {}
                context_object['pk'] = dot
                dot += 1
                context_object['model'] = 'location.countrysubdivision'
                context_object['fields'] = {}
                context_object['fields']['country'] = code_id
                context_object['fields']['name'] = country_tup[2]
                context_object['fields']['cn_name'] = country_tup[5]
                context_object['fields']['code'] = '{}-{}'.format(
                    code, code_id)
                i += 1

                objects.append(context_object)

        return {
            'status_code': 200,
            'data': objects
        }


register('sql', 'city', CityResource)
register('sql', 'state', StateResource)
register('sql', 'country', CountryResource)
register('sql', 'location', LocationResource)
register('sql', 'hk', HKResource)
