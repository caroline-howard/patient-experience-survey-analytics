from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from openpyxl import load_workbook
from PIL import Image, ImageDraw, ImageFont


PROJECT = Path(__file__).resolve().parents[1]
WORKBOOK = PROJECT / "excel_dashboard" / "patient_discharge_experience_dashboard.xlsx"
ASSET_DIR = PROJECT / "assets" / "gifs"
SITE_ASSET_DIR = PROJECT / "site" / "assets" / "gifs"
TMP = Path("/private/tmp/qualtrics_excel_real_preview")

SOFFICE = Path("/Users/carolinehoward/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/soffice")
PDFTOPPM = Path("/Users/carolinehoward/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm")

SHEETS = ["README", "Dashboard", "Category_Detail", "Hospital_Detail"]
PRINT_AREAS = {
    "README": "A1:H23",
    "Dashboard": "A1:R24",
    "Category_Detail": "A1:H25",
    "Hospital_Detail": "A1:I45",
}
GIF_NAMES = {
    "README": "workbook-navigation.gif",
    "Dashboard": "dashboard-overview.gif",
    "Category_Detail": "category-detail.gif",
    "Hospital_Detail": "hospital-detail.gif",
}
LABELS = {
    "README": ("README", "Start-here page", "Workbook scope and navigation"),
    "Dashboard": ("Dashboard", "Statewide KPI overview", "Medicine Communication priority"),
    "Category_Detail": ("Category_Detail", "Submeasure breakdown", "Side-effect explanation spotlight"),
    "Hospital_Detail": ("Hospital_Detail", "Facility comparison", "Above/below Florida average"),
}


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial Bold.ttf" if bold else "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


CANVAS_W = 1920
CANVAS_H = 1080
BANNER_H = 108

TITLE_FONT = font(56, True)
SMALL_FONT = font(32)


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True, cwd=PROJECT)


def make_preview_workbook() -> Path:
    TMP.mkdir(parents=True, exist_ok=True)
    preview = TMP / "preview_only.xlsx"
    wb = load_workbook(WORKBOOK)
    keep = set(SHEETS)
    for ws in list(wb.worksheets):
        if ws.title not in keep:
            wb.remove(ws)
    for ws in wb.worksheets:
        ws.print_area = PRINT_AREAS.get(ws.title, ws.calculate_dimension())
        ws.page_setup.orientation = "landscape"
        ws.page_setup.fitToWidth = 1
        ws.page_setup.fitToHeight = 1
        ws.sheet_properties.pageSetUpPr.fitToPage = True
    wb.save(preview)
    return preview


def export_pdf(preview: Path) -> Path:
    pdf_dir = TMP / "preview_pdf"
    profile = TMP / "lo-profile"
    shutil.rmtree(pdf_dir, ignore_errors=True)
    shutil.rmtree(profile, ignore_errors=True)
    pdf_dir.mkdir(parents=True, exist_ok=True)
    run(
        [
            str(SOFFICE),
            f"-env:UserInstallation=file://{profile}",
            "--headless",
            "--convert-to",
            "pdf",
            "--outdir",
            str(pdf_dir),
            str(preview),
        ]
    )
    return pdf_dir / "preview_only.pdf"


def render_pages(pdf: Path) -> list[Path]:
    pages = TMP / "preview_pages"
    shutil.rmtree(pages, ignore_errors=True)
    pages.mkdir(parents=True, exist_ok=True)
    run([str(PDFTOPPM), "-png", "-r", "240", str(pdf), str(pages / "page")])
    return sorted(pages.glob("page-*.png"))


def fit_page(path: Path) -> Image.Image:
    page = Image.open(path).convert("RGB")
    # Trim the PDF page margin while preserving the real rendered sheet content.
    pixels = page.load()
    xs: list[int] = []
    ys: list[int] = []
    for y in range(page.height):
        for x in range(page.width):
            r, g, b = pixels[x, y]
            if r < 245 or g < 245 or b < 245:
                xs.append(x)
                ys.append(y)
    if xs and ys:
        pad = 18
        page = page.crop(
            (
                max(min(xs) - pad, 0),
                max(min(ys) - pad, 0),
                min(max(xs) + pad, page.width),
                min(max(ys) + pad, page.height),
            )
        )
    page.thumbnail((1760, 900), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (CANVAS_W, CANVAS_H), "#f6f8fa")
    x = (CANVAS_W - page.width) // 2
    y = BANNER_H + (CANVAS_H - BANNER_H - page.height) // 2
    canvas.paste(page, (x, y))
    return canvas


def add_banner(frame: Image.Image, sheet_name: str, active: int) -> Image.Image:
    title, line_one, line_two = LABELS[sheet_name]
    subtitle = line_one if active % 2 == 0 else line_two
    draw = ImageDraw.Draw(frame)
    draw.rectangle((0, 0, CANVAS_W, BANNER_H), fill="#155e75")
    draw.text((48, 24), title, fill="white", font=TITLE_FONT)
    draw.text((48, 74), subtitle, fill="#d5edf2", font=SMALL_FONT)
    return frame


def frames_for_page(path: Path, sheet_name: str) -> list[Image.Image]:
    base = fit_page(path)
    frames: list[Image.Image] = []
    for i in range(4):
        frame = base.copy()
        add_banner(frame, sheet_name, i)
        if i in (1, 2):
            crop = frame.crop((120, 130, 1800, 990))
            crop.thumbnail((CANVAS_W, CANVAS_H - 88), Image.Resampling.LANCZOS)
            zoom = Image.new("RGB", (CANVAS_W, CANVAS_H), "#f6f8fa")
            zoom.paste(crop, ((CANVAS_W - crop.width) // 2, BANNER_H))
            add_banner(zoom, sheet_name, i)
            frame = zoom
        frames.append(frame)
    return frames


def save_gif(frames: list[Image.Image], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(
        path,
        save_all=True,
        append_images=frames[1:] + frames[-2:0:-1],
        duration=1000,
        loop=0,
        optimize=True,
    )


def main() -> None:
    if not SOFFICE.exists() or not PDFTOPPM.exists():
        raise SystemExit("LibreOffice/pdftoppm runtime not found.")
    preview = make_preview_workbook()
    pdf = export_pdf(preview)
    pages = render_pages(pdf)
    if len(pages) != len(SHEETS):
        raise SystemExit(f"Expected {len(SHEETS)} rendered pages, found {len(pages)}")
    for sheet_name, page in zip(SHEETS, pages):
        frames = frames_for_page(page, sheet_name)
        for base_dir in [ASSET_DIR, SITE_ASSET_DIR]:
            output = base_dir / GIF_NAMES[sheet_name]
            save_gif(frames, output)
            print(f"{output.relative_to(PROJECT)} {output.stat().st_size}")


if __name__ == "__main__":
    main()
