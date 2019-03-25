import logging
from lead import Lead
import json
import sys
import getopt


class DedupeError(Exception):
    pass


class LeadDeduper(object):
    """
    Removes duplicates from a list of leads, where duplicates are defined by leads with the same email or id.
    In the case where two leads are determined to be duplicates, include the one that has the most recent entry date.
    In the case where two duplicate leads have the same entry date, include the one that occurs later in the list.
    """

    def __init__(self):
        self.logger = logging.getLogger()
        logging.basicConfig(filename='dedupe.log', level=logging.INFO)

    def dedupe_leads(self, infile, outfile):
        out_list = self._parse_infile(infile)
        deduped_list = self._remove_duplicates(out_list)
        self._write_to_outfile(deduped_list, outfile)

    def _parse_infile(self, infile):
        # parses the input file and returns a list of lead objects sorted by date
        write_list = []
        with open(infile) as json_file:
            data = json.load(json_file)
            if data.get("leads") is None:
                raise DedupeError("Input file is incorrectly formatted. 'leads' field is required")
            for lead in data["leads"]:
                write_list.append(Lead(lead))
        return sorted(write_list, key=lambda l: l.datetime(), reverse=True)

    def _remove_duplicates(self, leads):
        # removes duplicate leads, where two leads are duplicates if they share either an ID or email
        out_list = []
        emails = set()
        ids = set()
        for l in leads:
            if l.id not in ids and l.email not in emails:
                out_list.append(l)
                emails.add(l.email)
                ids.add(l.id)
                self.logger.info("Including " + l.id + " with " + l.email + " in output.")
            else:
                self.logger.info("Not including " + l.id + " with " + l.email + " in output.")
        return out_list

    def _write_to_outfile(self, leads, outfile):
        with open(outfile, 'w') as f:
            json.dump({"leads": [l.to_dict() for l in leads]}, f)


if __name__ == "__main__":
    usage = "Usage: dedupe.py --infile=leads.json --outfile=deduped_leads.json"
    try:
        args, vals = getopt.getopt(sys.argv[1:], "hi:o:", ["help", "infile=", "outfile="])
    except getopt.error as error:
        print(usage)
        sys.exit(2)
    infile = None
    outfile = None
    for a, v in args:
        if a in ("-h", "--help"):
            print(usage)
        elif a in ("-i", "--infile"):
            infile = v
        elif a in ("-o", "--outfile"):
            outfile = v
    if infile is None or outfile is None:
        print("Must specify an input and output file.")
        print(usage)
        sys.exit(2)
    deduper = LeadDeduper()
    deduper.dedupe_leads(infile, outfile)
    print("Leads written to " + outfile)

