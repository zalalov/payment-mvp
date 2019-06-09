import inspect
import json
from aiohttp.web import Request, Response
from aiohttp.web import HTTPMethodNotAllowed, HTTPBadRequest, HTTPNotFound
from collections import OrderedDict

from database import session
from config import get_configuration

configuration = get_configuration()

DEFAULT_METHODS = ('GET', 'POST', 'PUT', 'DELETE')


class RestEndpoint:
    def __init__(self):
        self.methods = {}

        for method_name in DEFAULT_METHODS:
            method = getattr(self, method_name.lower(), None)
            if method:
                self.register_method(method_name, method)

    def register_method(self, method_name, method):
        self.methods[method_name.upper()] = method

    async def dispatch(self, request: Request):
        method = self.methods.get(request.method.upper())
        if not method:
            raise HTTPMethodNotAllowed('', DEFAULT_METHODS)

        wanted_args = list(inspect.signature(method).parameters.keys())
        available_args = request.match_info.copy()
        available_args.update({'request': request})

        unsatisfied_args = set(wanted_args) - set(available_args.keys())
        if unsatisfied_args:
            # Expected match info that doesn't exist
            raise HTTPBadRequest()

        return await method(**{arg_name: available_args[arg_name] for arg_name in wanted_args})


class CollectionEndpoint(RestEndpoint):
    def __init__(self, resource):
        super().__init__()
        self.resource = resource

    async def get(self):
        data = []

        # TODO: Port to limit & offset
        entities = session.query(self.resource.model).limit(10).all()

        for entity in entities:
            data.append(self.resource.render(entity))

        return Response(
            status=200,
            body=self.resource.encode({self.resource.name: [data, ]}),
            content_type=configuration.REST_DEFAULT_CONTENT_TYPE
        )

    async def post(self, request):
        data = await request.json()
        entity = self.resource.model.from_json(data)
        session.add(entity)
        session.commit()

        return Response(
            status=201,
            body=self.resource.encode({self.resource.name: [self.resource.render(entity), ]}),
            content_type=configuration.REST_DEFAULT_CONTENT_TYPE
        )


class InstanceEndpoint(RestEndpoint):
    def __init__(self, resource):
        super().__init__()
        self.resource = resource

    async def get(self, instance_id):
        instance = session.query(self.resource.model).filter(self.resource.model.id == instance_id).first()

        if not instance:
            return Response(
                status=404,
                body=json.dumps({'Not found': 404}),
                content_type=configuration.REST_DEFAULT_CONTENT_TYPE
            )

        data = self.resource.render_and_encode(instance)

        return Response(status=200, body=data, content_type=configuration.REST_DEFAULT_CONTENT_TYPE)

    async def put(self, request, instance_id):
        data = await request.json()

        entity = session.query(self.resource.model).filter(self.resource.model.id == instance_id).first()

        if not entity:
            raise HTTPNotFound()

        entity.update(**data)

        session.commit()
        session.refresh(entity)

        return Response(
            status=201,
            body=self.resource.render_and_encode(entity),
            content_type=configuration.REST_DEFAULT_CONTENT_TYPE
        )

    async def delete(self, instance_id):
        entity = session.query(self.resource.model).filter(self.resource.model.id == instance_id).first()

        if not entity:
            HTTPNotFound()

        session.delete(entity)
        session.commit()

        return Response(status=204)


class RestResource:
    def __init__(self, name, model, properties, id_field, prefix='/api'):
        self.name = name
        self.model = model
        self.properties = properties
        self.id_field = id_field
        self.prefix = prefix

        self.collection_endpoint = CollectionEndpoint(self)
        self.instance_endpoint = InstanceEndpoint(self)

    def register(self, router, prefix=''):
        router.add_route(
            '*',
            '{prefix}/{name}'.format(
                prefix=self.prefix,
                name=self.name
            ),
            self.collection_endpoint.dispatch
        )
        router.add_route(
            '*',
            '{prefix}/{name}/{{instance_id}}'.format(
                prefix=self.prefix,
                name=self.name
            ),
            self.instance_endpoint.dispatch
        )

    def render(self, instance):
        return OrderedDict((property, getattr(instance, property)) for property in self.properties)

    @staticmethod
    def encode(data):
        return json.dumps(data)

    def render_and_encode(self, instance):
        return self.encode(self.render(instance))
