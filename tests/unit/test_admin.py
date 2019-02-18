from django.contrib.admin import AdminSite
from django.contrib.auth.models import Group, User
from django.test.client import RequestFactory

import pytest
from katka.admin import (
    ApplicationAdmin, CredentialAdmin, CredentialSecretAdmin, ProjectAdmin, SCMServiceAdmin, TeamAdmin,
)
from katka.fields import username_on_model
from katka.models import Application, Credential, CredentialSecret, Project, SCMRepository, SCMService, Team


@pytest.fixture
def mock_request():
    factory = RequestFactory()
    request = factory.get('/')
    request.user = User(username='mock1')
    return request


@pytest.fixture
def group():
    g = Group(name='group1')
    g.save()
    return g


@pytest.fixture
def team(group):
    t = Team(name='team', group=group)
    with username_on_model(Team, 'audit_user'):
        t.save()
    return t


@pytest.fixture
def project(team):
    p = Project(name='project1', team=team)
    with username_on_model(Project, 'audit_user'):
        p.save()
    return p


@pytest.fixture
def credential(team):
    c = Credential(name='credential1', team=team)
    with username_on_model(Credential, 'audit_user'):
        c.save()
    return c


@pytest.fixture
def scm_service():
    scm_service = SCMService(type='bitbucket', server_url='www.example.com')
    with username_on_model(SCMService, 'audit_user'):
        scm_service.save()
    return scm_service


@pytest.fixture
def scm_repository(scm_service, credential):
    scm_repository = SCMRepository(scm_service=scm_service, credential=credential,
                                   organisation='acme', repository_name='sample')
    with username_on_model(SCMRepository, 'audit_user'):
        scm_repository.save()
    return scm_repository


@pytest.mark.django_db
class TestTeamAdmin:
    def test_save_stores_username(self, mock_request, group):
        t = TeamAdmin(Team, AdminSite())
        obj = Team(group=group)
        t.save_model(mock_request, obj, None, None)
        assert obj.created_username == 'mock1'
        assert obj.modified_username == 'mock1'


@pytest.mark.django_db
class TestProjectAdmin:
    def test_save_stores_username(self, mock_request, team):
        p = ProjectAdmin(Project, AdminSite())
        obj = Project(name='Project D', slug='PRJD', team=team)
        p.save_model(mock_request, obj, None, None)

        assert obj.created_username == 'mock1'
        assert obj.modified_username == 'mock1'


@pytest.mark.django_db
class TestApplicationAdmin:
    def test_save_stores_username(self, mock_request, project, scm_repository):
        a = ApplicationAdmin(Application, AdminSite())
        obj = Application(name='Application D', slug='APPD', project=project, scm_repository=scm_repository)
        a.save_model(mock_request, obj, None, None)

        assert obj.created_username == 'mock1'
        assert obj.modified_username == 'mock1'


@pytest.mark.django_db
class TestCredentialAdmin:
    def test_save_stores_username(self, mock_request, team):
        c = CredentialAdmin(Credential, AdminSite())
        obj = Credential(name='Credential D', slug='CRED', team=team)
        c.save_model(mock_request, obj, None, None)

        assert obj.created_username == 'mock1'
        assert obj.modified_username == 'mock1'


@pytest.mark.django_db
class TestCredentialSecretAdmin:
    def test_save_stores_username(self, mock_request, credential):
        c = CredentialSecretAdmin(CredentialSecret, AdminSite())
        obj = CredentialSecret(key='access_key', value='supersecret', credential=credential)
        c.save_model(mock_request, obj, None, None)

        assert obj.created_username == 'mock1'
        assert obj.modified_username == 'mock1'


@pytest.mark.django_db
class TestSCMServiceAdmin:
    def test_save_stores_username(self, mock_request):
        c = SCMServiceAdmin(SCMService, AdminSite())
        obj = SCMService(type='git', server_url='www.example.com')
        c.save_model(mock_request, obj, None, None)

        assert obj.created_username == 'mock1'
        assert obj.modified_username == 'mock1'