from django.db import models

from utils.webdriver import get_webdriver
from selenium.webdriver.common.by import By

from django.core.files.storage import storages

COUNTRIES = (
    ("es", "Spain"),
    ("de", "Germany"),
)


class RockenJobProfile(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=64)
    email = models.CharField(max_length=64)
    phone_country = models.CharField(max_length=5, choices=COUNTRIES)
    phone_number = models.CharField(max_length=32)
    actual_position = models.CharField(max_length=64, null=True, blank=True)
    link = models.URLField(max_length=128, blank=True, null=True)
    cv = models.FileField(upload_to="jobs", storage=storages["local"])
    certificates = models.FileField(upload_to="jobs", storage=storages["local"])
    extra_doc = models.FileField(
        upload_to="jobs", storage=storages["local"], null=True, blank=True
    )

    def __str__(self):
        return "%s %s, %s" % (self.first_name, self.last_name, self.actual_position)


class RockenJobSearch(models.Model):
    name = models.CharField(max_length=32)
    url = models.CharField(max_length=128)
    profile = models.ForeignKey(RockenJobProfile, on_delete=models.CASCADE)

    def __str__(self):
        return "%s for %s" % (self.name, str(self.profile))


class RockenJob(models.Model):
    recruiter = models.CharField(max_length=64, null=True)
    vacancy_url = models.CharField(max_length=1024)
    vacancy_id = models.CharField(max_length=16, unique=True)
    profile = models.ForeignKey(RockenJobProfile, on_delete=models.CASCADE, null=True)

    @classmethod
    def search_and_create(cls):
        driver = get_webdriver()
        jobs = []
        for search_obj in RockenJobSearch.objects.all():
            driver.get(search_obj.url)
            driver.implicitly_wait(10)

            results = driver.find_elements(By.CLASS_NAME, "result-item")

            for item in results:
                vacancy_id = item.get_attribute("data-vacancy_id")
                vacancy_url = item.get_attribute("href")
                if not cls.objects.filter(vacancy_id=vacancy_id).exists():
                    jobs.append(
                        cls(
                            vacancy_url=vacancy_url,
                            vacancy_id=vacancy_id,
                            profile=search_obj.profile,
                        )
                    )
        cls.objects.bulk_create(jobs)


class RockenJobApplication(models.Model):
    job = models.ForeignKey(RockenJob, on_delete=models.CASCADE, null=True)
    profile = models.ForeignKey(RockenJobProfile, on_delete=models.CASCADE, null=True)
    applied = models.BooleanField(default=False)

    def apply(self):
        driver = get_webdriver()
        driver.get(self.job.vacancy_url)
        driver.implicitly_wait(10)
        # click on apply
        driver.find_element(By.CLASS_NAME, "vacancy__apply").click()
        driver.implicitly_wait(2)
        # accept cookies
        driver.find_element(By.ID, "cn-accept-cookie").click()
        driver.implicitly_wait(2)
        driver.switch_to.window(driver.window_handles[1])
        driver.implicitly_wait(2)

        # Click on "Herr"
        driver.find_element(By.TAG_NAME, "label").click()
        driver.implicitly_wait(1)
        # Send fist_name
        driver.find_element(By.NAME, "Candidates[first_name]").send_keys(
            self.profile.first_name
        )
        driver.implicitly_wait(1)
        # Send last_name
        driver.find_element(By.NAME, "Candidates[last_name]").send_keys(
            self.profile.last_name
        )
        driver.implicitly_wait(1)
        # Send email
        driver.find_element(By.NAME, "Candidates[email]").send_keys(self.profile.email)
        driver.implicitly_wait(1)
        # number country code
        driver.find_element(By.CLASS_NAME, "iti__selected-flag").click()
        driver.implicitly_wait(1)

        driver.find_element(By.ID, "iti-item-%s" % self.profile.phone_country).click()
        driver.implicitly_wait(1)
        # number
        driver.find_element(By.NAME, "Candidates[part_phone]").send_keys(
            self.profile.phone_number
        )
        driver.implicitly_wait(1)
        # actual position
        driver.find_element(By.NAME, "Candidates[comment]").send_keys(
            self.profile.actual_position
        )
        driver.implicitly_wait(1)
        # link
        driver.find_element(By.NAME, "Candidates[external_profile_link]").send_keys(
            self.profile.link
        )
        driver.implicitly_wait(1)

        # upload cv!
        driver.find_element(By.ID, "dcup-field__type_cv").send_keys(
            self.profile.cv.path
        )
        driver.implicitly_wait(3)

        # upload document
        driver.find_element(By.ID, "dcup-field__type_references").send_keys(
            self.profile.certificates.path
        )
        # upload extra doc
        if self.profile.extra_doc:
            driver.find_element(By.ID, "dcup-field__type_references").send_keys(
                self.profile.extra_doc.path
            )

        driver.implicitly_wait(3)

        # accept
        driver.find_element(By.CLASS_NAME, "form__checkbox").click()
        driver.implicitly_wait(1)
        # send
        driver.find_element(By.CLASS_NAME, "primary-btn").click()
        driver.close()
        self.applied = True
        self.save()


def create_applications():
    profiles = RockenJobProfile.objects.all()
    jobs = RockenJob.objects.all()
    for p in profiles:
        for j in jobs:
            RockenJobApplication.objects.get_or_create(job=j, profile=p)
