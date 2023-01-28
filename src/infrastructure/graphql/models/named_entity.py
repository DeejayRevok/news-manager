from graphene import ObjectType, String


class NamedEntity(ObjectType):
    text = String(description="Named entity text")
    type = String(description="Named entity type")
