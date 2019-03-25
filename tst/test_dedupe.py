import unittest
import json
import os
from dedupe import LeadDeduper, DedupeError
from lead import Lead


class TestLeadDeduper(unittest.TestCase):
    def setUp(self):
        self.deduper = LeadDeduper()

    def tearDown(self):
        try:
            os.remove("tmp_test_outfile.json")
        except:
            pass

    def test_parse_infile(self):
        fname = "../leads.json"
        out_list = self.deduper._parse_infile(fname)
        self.assertEqual(len(out_list), 10)
        self.assertEqual(out_list[0].id, "vug789238jdsnfsj23")

    def test_remove_duplicates(self):
        leads = [
            Lead({
                "_id": "jkj238238jdsnfsj23",
                "email": "foo@bar.com",
                "firstName": "John",
                "lastName": "Smith",
                "address": "123 Street St",
                "entryDate": "2014-05-07T17:30:20+00:00"
            }),
            Lead({
                "_id": "jkj238238jdsnfsj23",
                "email": "mae@bar.com",
                "firstName": "Ted",
                "lastName": "Masters",
                "address": "44 North Hampton St",
                "entryDate": "2014-05-07T17:31:20+00:00"
            })
        ]
        outlst = self.deduper._remove_duplicates(leads)
        self.assertEqual(len(outlst), 1)
        self.assertEqual(outlst[0].email, "foo@bar.com")

    def test_remove_duplicates_no_dups(self):
        # should not modify list order in case of no duplicates
        leads = [
            Lead({
                "_id": "a",
                "email": "foo@bar.com",
                "firstName": "John",
                "lastName": "Smith",
                "address": "123 Street St",
                "entryDate": "2014-05-07T17:30:20+00:00"
            }),
            Lead({
                "_id": "b",
                "email": "mae@bar.com",
                "firstName": "Ted",
                "lastName": "Masters",
                "address": "44 North Hampton St",
                "entryDate": "2014-05-07T17:31:20+00:00"
            })
        ]
        outlst = self.deduper._remove_duplicates(leads)
        self.assertEqual(len(outlst), 2)
        self.assertEqual(outlst[0].email, "foo@bar.com")
        self.assertEqual(outlst[1].email, "mae@bar.com")

    def test_dedupe_leads_dedupe_error(self):
        self.assertRaises(DedupeError, self.deduper.dedupe_leads, "malformed_leads.json", "../deduped.json")

    def test_dedupe_leads(self):
        self.deduper.dedupe_leads("../leads.json", "tmp_test_outfile.json")
        j1 = json.load(open("tmp_test_outfile.json"))
        j2 = json.load(open("expected.json"))
        self.assertEquals(len(j1["leads"]), len(j2["leads"]))
        for i in range(len(j1["leads"])):
            self.assertEquals(j1["leads"][i], j2["leads"][i])


if __name__ == '__main__':
    unittest.main()
