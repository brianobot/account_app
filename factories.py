import factory
from accounts.models import User, Profile


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('email',)
    
    email = factory.Sequence(lambda n: f"user_{n}@example.com")
    password = 'testpassword12secure'


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile
        django_get_or_create = ('user',)

    #the addition of profile=None is a measure to fix duplicate user keys in factory boy
    user = factory.SubFactory(UserFactory, profile=None) 
    bio = 'default user bio'
    