import datetime
import os
from io import BytesIO

import requests
from bs4 import BeautifulSoup
from PIL import Image


class DownloadImage:
    def __init__(self, page_url, outdir):
        assert isinstance(page_url, str)
        assert isinstance(outdir, str)

        if not os.path.exists(outdir):
            os.makedirs(outdir)

        self.outdir = outdir
        self.today = datetime.date.today()
        r = requests.get(page_url)
        self.soup = BeautifulSoup(r.text, features="html.parser")

    def get_image_url(self):
        self.img_urls = []
        for img_tag in self.soup.find_all("img"):
            url = img_tag.get("src")
            if url is not None:
                self.img_urls.append(url)
        return self.img_urls

    def download_image(self, url, file_path, resize=None):
        assert isinstance(url, str)
        assert isinstance(file_path, str)
        assert isinstance(resize, int) or resize is None

        r = requests.get(url, stream=True)
        if r.status_code == 200:
            img = Image.open(BytesIO(r.content))
            if resize is not None:
                alpha = resize / min(img.width, img.height)
                width = int(img.width * alpha)
                height = int(img.height * alpha)
                img = img.resize((width, height))
            img.save(file_path)

    def scrape(self, keyword=None, suffix=None, resize=None):
        assert isinstance(keyword, str) or keyword is None
        assert isinstance(suffix, str) or suffix is None
        assert isinstance(resize, int) or resize is None

        n = 0
        for url in self.img_urls:
            if self.select_image(url, keyword=keyword, suffix=suffix):
                n += 1
                file_name = f"{self.today}_{n}.jpg"
                file_path = os.path.join("output", file_name)
                self.download_image(url, file_path, resize=resize)
                print(f">> {file_path}")

    def select_image(self, url, keyword=None, suffix=None):
        assert isinstance(url, str)
        assert isinstance(keyword, str) or keyword is None
        assert isinstance(suffix, str) or suffix is None

        is_download = url.endswith(".jpg") or url.endswith(".png")
        if keyword is not None:
            is_download = keyword in url
        if suffix is not None:
            is_download = url.endswith(suffix)

        return is_download


def download_image(page_url, outdir, keyword, suffix, resize):
    print(f"Page URL: {page_url}")
    print(f"Output directory: {outdir}")
    print(f"Keyword: {keyword}")
    print(f"Suffix: {suffix}")
    print(f"Resize: {resize}")

    process = DownloadImage(page_url, outdir)
    process.get_image_url()
    process.scrape(keyword=keyword, suffix=suffix, resize=resize)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument("page_url", type=str, help="web page URL.")
    parser.add_argument("outdir", type=str, help="path of output directory.")
    parser.add_argument(
        "--keyword", type=str, default=None, help="keyword in URL of download images."
    )
    parser.add_argument(
        "--suffix", type=str, default=None, help="file type of download images."
    )
    parser.add_argument(
        "--resize", type=int, default=None, help="max length of output images."
    )

    args = parser.parse_args()

    download_image(args.page_url, args.outdir, args.keyword, args.suffix, args.resize)
