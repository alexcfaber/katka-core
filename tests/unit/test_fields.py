from django.db import models

import pytest
from katka.exceptions import MissingUsername
from katka.fields import AutoUsernameField, username_on_model


class AlwaysUpdate(models.Model):
    field = AutoUsernameField()

    class Meta:
        app_label = 'katka'


class OnlyOnCreate(models.Model):
    field = AutoUsernameField(only_on_create=True)

    class Meta:
        app_label = 'katka'


@pytest.mark.django_db
class TestAutoUsername:
    def test_missing_context_manager(self):
        model = AlwaysUpdate()
        with pytest.raises(MissingUsername) as e:
            model.save()

        assert 'username_on_model(AlwaysUpdate, username)' in e.value.args[0]

    def test_always_update(self):
        model = AlwaysUpdate()
        with username_on_model(AlwaysUpdate, 'test_user'):
            model.save()

        assert model.field == 'test_user'

        with username_on_model(AlwaysUpdate, 'user2'):
            model.save()

        assert model.field == 'user2'

    def test_only_on_create(self):
        model = OnlyOnCreate()
        with username_on_model(OnlyOnCreate, 'test_user'):
            model.save()

        assert model.field == 'test_user'

        with username_on_model(OnlyOnCreate, 'user2'):
            model.save()

        assert model.field == 'test_user'
