import json

from django.core.management.base import BaseCommand

from one.companies.models import Company, CompanyLocation, Person
from one.geo.models import GoogleGeoInfo as Geo
from one.socialmedia.models import LinkedinChannel, LinkedinGroupChannel


class Command(BaseCommand):
    help = "Load data from json file"

    def add_arguments(self, parser):
        parser.add_argument("filename", nargs=1, type=str)

    def handle(self, *args, **options):
        filename = options.get("filename")[0]

        with open(filename) as file:
            data = json.load(file)

        companies_dict = {}

        company_data_list = [d for d in data if d.get("model") == "jobs.company"]
        linkedin_group_list = [
            d for d in data if d.get("model") == "socialmedia.linkedingroup"
        ]

        li_channel = LinkedinChannel.objects.filter(author_type="person").first()
        if not li_channel:
            self.stderr.write("No Linkedin channel available to set to group channels.")

        for group_data in linkedin_group_list:
            fields_dict = group_data.get("fields")
            LinkedinGroupChannel.objects.get_or_create(
                channel=li_channel,
                group_id=fields_dict["group_id"],
                is_private=fields_dict["private"],
                is_active=fields_dict["active"],
                name=fields_dict["name"],
                language=fields_dict["language"],
            )

        for company_data in company_data_list:
            fields_dict = company_data.get("fields")
            company = Company.objects.get_or_create(name=fields_dict.get("name"))[0]
            companies_dict[company_data.get("pk")] = company
            geo = Geo.objects.get_or_create(address=fields_dict.get("address"))[0]
            CompanyLocation.objects.get_or_create(company=company, geo_info=geo)

        recruiter_data_list = [d for d in data if d.get("model") == "jobs.recruiter"]
        for recruiter_data in recruiter_data_list:
            fields_dict = recruiter_data.get("fields")
            recruiter_company = companies_dict[fields_dict.get("company")]

            fullname: str = fields_dict.get("name")
            fullname_list = fullname.split()
            if len(fullname_list) == 2:
                first_name, last_name = fullname_list
            elif len(fullname_list) < 2:
                first_name = fullname
                last_name = fullname
            else:
                first_name = fullname_list[0]
                last_name = " ".join(fullname_list[1:])

            Person.objects.get_or_create(
                is_hr=True,
                company=recruiter_company,
                gender=fields_dict.get("gender"),
                first_name=first_name,
                last_name=last_name,
                email=fields_dict.get("email"),
                phone=fields_dict.get("phone"),
                remarks=fields_dict.get("remarks"),
            )
