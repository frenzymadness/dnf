import base
import dnf.queries
import hawkey
import unittest

class Queries(unittest.TestCase):
    def test_duplicities(self):
        yumbase = base.mock_yum_base()
        pepper = dnf.queries.installed_by_name(yumbase.sack, "pepper")
        # make sure 'pepper' package exists:
        self.assertEqual(len(pepper), 1)
        # we shouldn't see it more than once with a tricky query below:
        res = dnf.queries.installed_by_name(yumbase.sack, ["pep*", "*per"])
        res_set = set(res)
        self.assertEqual(len(res), len(res_set))

    def test_by_file(self):
        # check sanity first:
        yumbase = base.mock_yum_base()
        q = hawkey.Query(yumbase.sack)
        q.filter(file__eq="/raised/smile")
        self.assertEqual(len(q.run()), 1)
        pkg = q.result[0]

        # now the query:
        yumbase = base.mock_yum_base()
        res = dnf.queries.by_file(yumbase.sack, "/raised/smile")
        self.assertEqual(len(res), 1)
        self.assertEqual(pkg, res[0])

    def test_by_repo(self):
        yumbase = base.mock_yum_base("updates", "main")
        pkgs = dnf.queries.by_repo(yumbase.sack, "updates")
        self.assertEqual(len(pkgs), base.UPDATES_NSOLVABLES)
        pkgs = dnf.queries.by_repo(yumbase.sack, "main")
        self.assertEqual(len(pkgs), base.MAIN_NSOLVABLES)

    def test_installed_exact(self):
        sack = base.mock_yum_base().sack
        pkgs = dnf.queries.installed_exact(sack, "tour", "4.9-0", "noarch")
        self.assertEqual(len(pkgs), 0)
        pkgs = dnf.queries.installed_exact(sack, "tour", "5-0", "x86_64")
        self.assertEqual(len(pkgs), 0)
        pkgs = dnf.queries.installed_exact(sack, "tour", "5-0", "noarch")
        self.assertEqual(len(pkgs), 1)
