from tortoise import Model, fields


class Group(Model):
    name = fields.CharField(max_length=10)

    users: fields.ReverseRelation["User"]


class User(Model):
    name = fields.CharField(max_length=20)
    group: fields.ForeignKeyRelation[Group] = fields.ForeignKeyField(
        "models.Group", on_delete=fields.OnDelete.CASCADE, related_name="users"
    )
