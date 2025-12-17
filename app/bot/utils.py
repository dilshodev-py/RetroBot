from db.models import User


def user_exists_or_create(user):
    users: [User] = User(id=user.id).get()
    if not users:
        u = {
            "id" : user.id,
            "first_name" : user.first_name,
            "last_name" : user.last_name,
        }
        User(**u).save()


