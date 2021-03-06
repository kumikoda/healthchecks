from hc.api.models import Check
from hc.test import BaseTestCase


class AddCheckTestCase(BaseTestCase):

    def test_it_works(self):
        url = "/checks/add/"
        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url)
        self.assertRedirects(r, "/checks/")
        check = Check.objects.get()
        self.assertEqual(check.project, self.project)

    def test_it_handles_unset_current_project(self):
        self.profile.current_project = None
        self.profile.save()

        url = "/checks/add/"
        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url)
        self.assertRedirects(r, "/checks/")
        check = Check.objects.get()
        self.assertEqual(check.project, self.project)

    def test_team_access_works(self):
        url = "/checks/add/"
        self.client.login(username="bob@example.org", password="password")
        self.client.post(url)

        check = Check.objects.get()
        # Added by bob, but should belong to alice (bob has team access)
        self.assertEqual(check.project, self.project)

    def test_it_rejects_get(self):
        url = "/checks/add/"
        self.client.login(username="alice@example.org", password="password")
        r = self.client.get(url)
        self.assertEqual(r.status_code, 405)

    def test_it_obeys_check_limit(self):
        self.profile.check_limit = 0
        self.profile.save()

        url = "/checks/add/"
        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url)
        self.assertEqual(r.status_code, 400)
