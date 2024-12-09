import os
import time
import zipfile
from pathlib import Path
from typing import List

from datafiles import datafile
from django.conf import settings
from django.utils.functional import cached_property
from etsyv3.enums import ListingType, WhoMade
from etsyv3.models.file_request import (
    UploadListingFileRequest,
    UploadListingImageRequest,
)
from etsyv3.models.listing_request import CreateDraftListingRequest
from pdf2image import convert_from_path as convert_pdf_from_path
from PIL import Image

from auths.models import Etsy
from tex.compile import render_pdf as latex_render_pdf
from utils.telegram import report_to_admin
from utils.webdrivers import Gumroad

LISTINGS_PATH = settings.BASE_DIR / "material" / "listings"
COMMON_PATH = settings.BASE_DIR / "material" / "listings_common"

ETSY_TAXNOMY_IDS = {
    "calendar": 2078,  # Digital Prints
}


class ListingInitException(Exception):
    pass


class ListingException(Exception):
    pass


@datafile("./material/listings/{self.dirname}/datafile.json")
class Listing:
    keywords: str
    dirname: str
    price: float
    title: str
    listing_type: str
    lang: str
    tags: List[str]
    summary: str = ""
    quantity: int = 999
    etsy_id: int = 0
    etsy_url: str = ""
    gumroad_url: str = ""

    def __post_init__(self):
        if self.listing_type == "general":
            raise ListingInitException("Listing type 'general' is not accepted")

    def render_latex_file(
        self,
        template_name,
        filename,
        context={},
        subfolders=None,
        sreenshots=True,
        images=True,
        run_times=1,
    ):
        """Generate a pdf from latex template and generate screenshots and images"""
        if subfolders:
            filepath = self.files_path / subfolders / filename
        else:
            filepath = self.files_path / filename

        filepath.parent.mkdir(exist_ok=True, parents=True)

        with open(filepath, "wb") as f:
            f.write(latex_render_pdf(template_name, context, run_times=run_times))
        if sreenshots:
            self.create_sreenshots(subfolders=subfolders)
        if images:
            self.generate_images_from_screenshots(subfolders=subfolders)

    def create_sreenshots(self, subfolders: str = None):
        """Create screenshots from the pdf"""
        # Calculate where to save the screenshots
        ss_path = (
            self.screenshots_path / subfolders if subfolders else self.screenshots_path
        )
        ss_path.mkdir(exist_ok=True, parents=True)

        if any(ss_path.iterdir()):
            print(f"⚠️ Directory {ss_path} is not empty.")

        # Calculate where to get the pdf files
        files_path = self.files_path / subfolders if subfolders else self.files_path

        pdf_paths = (p for p in files_path.iterdir() if str(p).endswith(".pdf"))
        for pdf_path in pdf_paths:
            convert_pdf_from_path(
                pdf_path=pdf_path, output_folder=ss_path, fmt="png", dpi=300
            )

    def generate_images_from_screenshots(self, subfolders: str = None):
        bg = Image.open(self.background_path)
        bg_w, bg_h = bg.size
        screenshots_path = (
            self.screenshots_path / subfolders if subfolders else self.screenshots_path
        )
        self.images_path.mkdir(exist_ok=True, parents=True)

        if any(self.images_path.iterdir()):
            print(f"⚠️ Directory {self.images_path} is not empty.")

        out_subfolders = subfolders.replace("/", "_") + "_" if subfolders else ""
        for i, screenshot_path in enumerate(screenshots_path.iterdir(), start=1):
            pic = Image.open(screenshot_path)
            pic_w, pic_h = pic.size

            # Calculating the new size for the new picture
            k = 0.8  # scale factor
            if pic_w > pic_h:
                new_pic_w = int(k * bg_w)
                new_pic_h = int((k * bg_w / pic_w) * pic_h)
            else:
                new_pic_w = int((k * bg_h / pic_h) * pic_w)
                new_pic_h = int(k * bg_h)

            # Making a copy of the images and working with RGB
            bg_copy = bg.copy().convert("RGBA")
            pic_new = pic.copy().convert("RGBA").resize((new_pic_w, new_pic_h))

            # Pasting the new pic in the background
            bg_copy.paste(
                pic_new,
                (int(0.5 * (bg_w - new_pic_w)), int(0.7 * (bg_h - new_pic_h))),
            )
            bg_copy.save(self.images_path / f"{out_subfolders}{i}.png")

    def _zip_it(self, zipname, orig, dest, extensions):
        zipfilename = zipname if zipname.endswith(".zip") else f"{zipname}.zip"
        target_zip = zipfile.ZipFile(os.path.join(dest, zipfilename), "w")
        for dp, dn, fn in os.walk(orig):
            for filename in fn:
                if filename.endswith(extensions):
                    target_zip.write(
                        os.path.join(dp, filename),
                        os.path.relpath(os.path.join(dp, filename), orig),
                    )
        target_zip.close()

    def zip_files(self, zipname: str, extensions: tuple = (".pdf",)):
        dest = str(self.files_path)
        orig = str(self.files_path)
        self._zip_it(zipname, orig, dest, extensions)

    def zip_screenshots(self, zipname="screenshots.zip", extensions: tuple = (".png",)):
        dest = str(self.screenshots_path)
        orig = str(self.screenshots_path)
        self._zip_it(zipname, orig, dest, extensions)

    # Path properties
    @cached_property
    def path(self) -> Path:
        """Listing path"""
        return LISTINGS_PATH / self.dirname

    @cached_property
    def files_path(self) -> Path:
        return self.path / "files"

    @cached_property
    def images_path(self) -> Path:
        return self.path / "images"

    @cached_property
    def screenshots_path(self) -> Path:
        return self.path / "screenshots"

    @cached_property
    def listing_type_images_path(self) -> Path:
        return COMMON_PATH / self.listing_type / self.lang

    @cached_property
    def note_path(self) -> Path:
        return COMMON_PATH / "general" / "note" / f"{self.lang}.png"

    @cached_property
    def readme_path(self) -> Path:
        d = {"en": "readme", "es": "leeme", "de": "liess-mich"}
        return COMMON_PATH / "general" / "readme" / f"{d[self.lang]}.txt"

    @cached_property
    def similar_products_path(self) -> Path:
        return COMMON_PATH / "general" / "similar_products" / f"{self.lang}.png"

    @cached_property
    def background_path(self) -> Path:
        return COMMON_PATH / self.listing_type / "background" / f"{self.lang}.png"

    def get_image_paths(self) -> List[Path]:
        if self.listing_type_images_path.exists():
            listing_type_images_paths = list(self.listing_type_images_path.iterdir())
        else:
            listing_type_images_paths = []
        return (
            list(self.images_path.iterdir())
            + listing_type_images_paths
            + [self.note_path, self.similar_products_path]
        )

    def get_file_paths(self):
        return [f for f in self.files_path.iterdir() if f.is_file()] + [
            self.readme_path
        ]

    # Description
    def get_description(self, title=True, general=True):
        content = self.title + "\n\n" if title else ""
        content += self.read_summary().strip() + "\n\n"
        if general:
            content += self.read_general_description().strip()
        return content

    def read_general_description(self):
        p = COMMON_PATH / "general" / "description" / f"{self.lang}.txt"
        with open(p, "r", encoding="utf8") as f:
            return f.read()

    def read_summary(self):
        with open(self.path / "summary.txt", "r", encoding="utf8") as f:
            return f.read()

    def write_summary(self, summary: str):
        with open(self.path / "summary.txt", "w", encoding="utf8") as f:
            f.write(summary)

    # Etsy
    @cached_property
    def etsy_taxonomy_id(self):
        return 2078  # digital prints

    def upload_to_etsy(self):
        if settings.DEBUG:
            raise ListingException("Only allowed to upload on production!")

        etsy = Etsy.load()

        api = etsy.get_api_client()
        draft_request = CreateDraftListingRequest(
            quantity=self.quantity,
            title=self.keywords,
            description=self.get_description(),
            price=self.price,
            who_made=WhoMade.I_DID,
            when_made="2020_2024",
            taxonomy_id=self.etsy_taxonomy_id,
            listing_type=ListingType.DOWNLOAD,
            tags=self.tags,
        )
        response = api.create_draft_listing(shop_id=etsy.shop_id, listing=draft_request)
        if "listing_id" not in response:
            report_to_admin(f"Failed to create listing {self.dirname}\n{response.text}")
            return

        self.etsy_id = response["listing_id"]
        self.etsy_url = response["url"]

        # uploading images
        for rank, image_path in enumerate(self.get_image_paths(), start=1):
            with open(image_path, "rb") as f:
                api.upload_listing_image(
                    shop_id=etsy.shop_id,
                    listing_id=self.etsy_id,
                    listing_image=UploadListingImageRequest(
                        image_bytes=f.read(), rank=rank
                    ),
                )

        # uploading files
        for file_path in self.get_file_paths():
            with open(file_path, "rb") as f:
                api.upload_listing_file(
                    shop_id=etsy.shop_id,
                    listing_id=self.etsy_id,
                    listing_file=UploadListingFileRequest(
                        file_bytes=f.read(), name=file_path.name
                    ),
                )

    def set_gumroad_url(self):
        self.gumroad_url = "https://ramiboutas.gumroad.com/l/" + self.dirname

    def upload_to_gumroad(self, driver: Gumroad):
        driver.new_product(
            title=self.title,
            price=self.price,
            url_slug=self.dirname,
            description=self.get_description(),
            coverpath_str=str(self.images_path / "1.png"),
            filepaths_str=[str(p) for p in self.get_file_paths()],
        )


def validate_keywords(keywords=""):
    timeout = time.time() + 2
    while len(keywords) > 140:
        title_list = keywords.split(", ")
        title_list.pop()
        keywords = ", ".join(title_list)
        if time.time() > timeout:
            raise TimeoutError.add_note("Make sure you have commas in your keywords")

    return keywords


def validate_tags(tags: list[str] = []):
    out = [tag for tag in tags if len(tag) < 21][0:12]
    return list(set(out))
