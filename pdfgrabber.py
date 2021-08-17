import time
import urllib.request
import json
import os


class PDFGrabber:
    def __init__(self, school_id=120, major='Game Design & Interactive Media, B.S.', major_code='GDIM', delay=0.5):
        self.school_id = school_id
        self.major = major
        self.major_code = major_code
        self.delay = delay

    def get_agreements(self):
        with urllib.request.urlopen(f'https://assist.org/api/institutions/{self.school_id}/agreements') as url:
            data = json.loads(url.read().decode())
        agreement_list = []
        for agreement in list(data):
            if agreement['isCommunityCollege']:
                school_id = agreement['institutionParentId']
                year = agreement['sendingYearIds'][-1]
                curr = {'id': school_id, 'year': year}
                agreement_list.append(curr)
        return agreement_list

    def get_keys(self):
        agreement_list = self.get_agreements()
        keys = []
        for agreement in agreement_list:
            time.sleep(self.delay)
            school_id, year = agreement['id'], agreement['year']
            with urllib.request.urlopen(
                    f'https://assist.org/api/agreements?receivingInstitutionId={self.school_id}' + 
                    f'&sendingInstitutionId={school_id}&academicYearId={year}&categoryCode=major'
            ) as url:
                data = json.loads(url.read().decode())
            data = data['reports']
            for report in list(data):
                if report['label'] == self.major:
                    keys.append({'key': report['key'], 'school_id': school_id})
        return keys

    def get_pdfs(self):
        keys = self.get_keys()
        for key in keys:
            key_val = key['key']
            school_id = key['school_id']
            pdf_url = f'https://assist.org/api/artifacts/{key_val}'
            file_name = f'agreements/report_{self.school_id}_{school_id}_{self.major_code}.pdf'
            os.makedirs(os.path.dirname(file_name), exist_ok=True)
            with open(file_name, 'wb') as f:
                f.write(urllib.request.urlopen(pdf_url).read())
            time.sleep(self.delay)
