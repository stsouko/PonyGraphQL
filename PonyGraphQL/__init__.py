from graphql import (GraphQLSchema, GraphQLObjectType, GraphQLField, GraphQLString, GraphQLArgument, GraphQLNonNull,
                     GraphQLInt, graphql)


def searcher(f):
    f._is_searcher_ = True
    return f


def get_query(db):
    objects = {}
    fields = {}
    for name in db.entities:
        attrs = {}
        fields[name] = attrs
        objects[name] = GraphQLObjectType(name, attrs)

    for name, entity in db.entities.items():
        attrs = fields[name]
        for k, v in entity._adict_.items():
            if v.is_relation:  # relations
                if v.is_collection:
                    if v.reverse.is_collection:  # many to many
                        pass
                    else:  # many to one
                        pass
                else:  # one to one
                    ql_type = objects[v.reverse.entity.__name__]
                    if v.is_required:
                        ql_type = GraphQLNonNull(ql_type)
                    attrs[k] = GraphQLField(ql_type, resolver=lambda root, info: getattr(root, info.field_name))
            else:  # just data fields
                ql_type = type_map[v.py_type]
                if v.is_required:
                    ql_type = GraphQLNonNull(ql_type)
                attrs[k] = GraphQLField(ql_type)

    fields = {}
    for name, obj in objects.items():
        fields[name] = GraphQLField(obj, args={'id': GraphQLArgument(GraphQLNonNull(GraphQLInt))},
                                    resolver=(lambda x: lambda root, info, **args: x[args['id']])(db.entities[name]))

    return GraphQLSchema(query=GraphQLObjectType(name='Query', fields=fields))


type_map = {int: GraphQLInt, str: GraphQLString}


__all__ = ['searcher', 'get_query']
