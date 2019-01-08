
db = Database()


class User(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    age = Optional(int, nullable=True)
    pseudo = Optional('Pseudo')

    @classmethod
    @searcher
    def search_name(cls, name):
        return cls.select(lambda x: x.name == name)[:]


#    groups = Set('Group')

# class Group(db.Entity):
#    id = PrimaryKey(int, auto=True)
#    name = Required(str)
#    users = Set('User')


class Pseudo(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    user = Required('User')


db.bind('sqlite', ':memory:')
db.generate_mapping(create_tables=True)

with db_session:
    u1 = User(name='vasya', age=12)
    u2 = User(name='pupkin', age=21)
    Pseudo(name='vasyan', user=u1)
#    g = Group(name='lohs')
#    g.users.add(u1)
#    g.users.add(u2)

set_sql_debug(True, True)

xxx = get_graphql(db)
with db_session:
    result = graphql(xxx, 'query {User (id: 1) {name pseudo {name}}}')
print(result.errors)
print(dumps(result.data, indent=2))
with db_session:
    result = graphql(xxx, 'query {User (id: 2) {name pseudo {name}}}')
print(result.errors)
print(dumps(result.data, indent=2))
with db_session:
    result = graphql(xxx, 'query {Pseudo (id: 1) {name user {name}}}')
print(result.errors)
print(dumps(result.data, indent=2))