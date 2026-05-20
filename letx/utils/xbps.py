from PIL.ImageFont import truetype
from pygame.examples.sprite_texture import tex
import subprocess

try:
    def xbps_src():
        result = subprocess.run(
                ["sh", "../backend/xbps-src"],
                capture_output=True,
                text=True
                )
        print(result.stdout)

    def binary_bootstrap():
        result = subprocess.run(
                ["sh", "../backend/xbps-src", "binary-bootstrap"],
                capture_output=True,
                text=True
                )
        print(result.stdout)

    def bootstrap():
        result = subprocess.run(
                ["sh", "../backend/xbps-src", "bootstrap"],
                capture_output=True,
                text=True
                )
        print(result.stdout)

    def bootstrap_update():
        result = subprocess.run(
                ["sh", "../backend/xbps-src", "bootstrap-update"],
                capture_output=True,
                text=True
                )
        print(result.stdout)

    def consistency_check():
        result = subprocess.run(
                ["sh", "../backend/xbps-src", "consistency-check"],
                capture_output=True,
                text=True
                )
        print(result.stdout)

    def chroot():
        result = subprocess.run(
                ["sh", "../backend/xbps-src", "chroot"],
                capture_output=True,
                text=True
                )
        print(result.stdout)

    def clean_repocache():
        result = subprocess.run(
                ["sh", "../backend/xbps-src", "clean-repocache"],
                capture_output=True,
                text=True
                )
        print(result.stdout)

    def fetch():
        result = subprocess.run(
                ["sh", "../backend/xbps-src", "fetch"],
                capture_output=True,
                text=True
                )
        print(result.stdout)

    def extract():
        result = subprocess.run(
                ["sh", "../backend/xbps-src", "extract"],
                capture_output=True,
                text=True
                )
        print(result.stdout)

    def patch():
        result = subprocess.run(
                ["sh", "../backend/xbps-src", "patch"],
                capture_output=True,
                text=True
                )
        print(result.stdout)

    def configure():
        result = subprocess.run(
                ["sh", "../backend/xbps-src", "configure"],
                capture_output=True,
                text=True
                )
        print(result.stdout)

    def build():
        result = subprocess.run(
                ["sh", "../backend/xbps-src", "build"],
                capture_output=True,
                text=True
                )
        print(result.stdout)

    def check():
        result = subprocess.run(
                ["sh", "../backend/xbps-src", "check"],
                capture_output=True,
                text=True
                )
        print(result.stdout)

    def install():
        result = subprocess.run(
                ["sh", "../backend/xbps-src", "install"],
                capture_output=True,
                text=True
                )
        print(result.stdout)

    def pkg():
        result = subprocess.run(
                ["sh", "../backend/xbps-src", "pkg"],
                capture_output=True,
                text=True
                )
        print(result.stdout)

    def clean():
        result = subprocess.run(
                ["sh", "../backend/xbps-src", "clean"],
                capture_output=True,
                text=True
                )

    def list():
        result = subprocess.run(
                ["sh", "../backend/xbps-src", "list"],
                capture_output=True,
                text=True
                )
        print(result.stdout)

    def remove():
        result = subprocess.run(
                ["sh", "../backend/xbps-src", "remove"],
                capture_output=True,
                text=True
                )
        print(result.stdout)

    def usage():
        result = subprocess.run(
                ["sh", "../backend/xbps-src", "-h"],
                capture_output=True,
                text=True
                )
        print(result.stdout)

    def verboseMessage():
        result = subprocess.run(
                ["sh", "../backend/xbps-src", "-v"],
                capture_output=True,
                text=True
                )
        print(result.stdout)

    def version():
        result = subprocess.run(
                ["sh", "../backend/xbps-src", "-V"],
                capture_output=True,
                text=True
                )
        print(result.stdout)

    except subprocess.CalledProcessError as e:
        print(f"Error Details :\n{e.stderr}")
