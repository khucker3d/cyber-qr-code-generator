# fancy_pants_qr_gui.py
#
# Mac install:
# pip3 install "qrcode[pil]"
#
# Windows install:
# py -m pip install "qrcode[pil]"

import os
import textwrap
import qrcode
import tkinter as tk

from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw, ImageFont


# =========================================================
# DEFAULT STYLE SETTINGS
# =========================================================

QR_FILL_COLOR = "#111111"
QR_BACK_COLOR = "#F7F7F7"
TEXT_COLOR = "#111111"
CARD_BACKGROUND = "#FFFFFF"
CARD_BORDER_COLOR = "#D0D0D0"

BOX_SIZE = 10
BORDER = 4
LOGO_SCALE = 0.22
CARD_PADDING = 30
LABEL_TOP_PADDING = 18
SUBTEXT_TOP_PADDING = 8
CARD_CORNER_RADIUS = 24
CARD_BORDER_WIDTH = 2


# =========================================================
# QR GENERATION HELPERS
# =========================================================

def load_font(size: int):
    candidate_fonts = [
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Helvetica.ttc",
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/calibri.ttf",
        "arial.ttf",
        "DejaVuSans.ttf",
    ]

    for font_path in candidate_fonts:
        try:
            return ImageFont.truetype(font_path, size)
        except Exception:
            continue

    return ImageFont.load_default()


TITLE_FONT = load_font(30)
SUBTEXT_FONT = load_font(20)


def get_text_size(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def wrap_text(text: str, width: int) -> list[str]:
    lines = []

    for part in text.split("\n"):
        wrapped = textwrap.wrap(part, width=width)
        lines.extend(wrapped if wrapped else [""])

    return lines


def build_qr_image(url: str) -> Image.Image:
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=BOX_SIZE,
        border=BORDER,
    )

    qr.add_data(url)
    qr.make(fit=True)

    return qr.make_image(
        fill_color=QR_FILL_COLOR,
        back_color=QR_BACK_COLOR
    ).convert("RGB")


def resize_logo(logo: Image.Image, qr_size: int) -> Image.Image:
    target_size = int(qr_size * LOGO_SCALE)
    logo = logo.copy()
    logo.thumbnail((target_size, target_size), Image.LANCZOS)
    return logo


def add_center_logo(qr_img: Image.Image, logo_path: str | None) -> Image.Image:
    if not logo_path:
        return qr_img

    if not os.path.exists(logo_path):
        return qr_img

    try:
        logo = Image.open(logo_path).convert("RGBA")
    except Exception:
        return qr_img

    qr_rgba = qr_img.convert("RGBA")
    qr_w, qr_h = qr_rgba.size

    logo = resize_logo(logo, qr_w)
    lx, ly = logo.size

    x = (qr_w - lx) // 2
    y = (qr_h - ly) // 2

    backing_padding = 12
    backing = Image.new(
        "RGBA",
        (lx + backing_padding * 2, ly + backing_padding * 2),
        (255, 255, 255, 0)
    )

    backing_draw = ImageDraw.Draw(backing)
    backing_draw.rounded_rectangle(
        (0, 0, backing.size[0] - 1, backing.size[1] - 1),
        radius=18,
        fill=(255, 255, 255, 255)
    )

    qr_rgba.alpha_composite(backing, (x - backing_padding, y - backing_padding))
    qr_rgba.alpha_composite(logo, (x, y))

    return qr_rgba.convert("RGB")


def create_qr_card(label: str, subtext: str, url: str, logo_path: str | None) -> Image.Image:
    qr_img = build_qr_image(url)
    qr_img = add_center_logo(qr_img, logo_path)

    qr_w, qr_h = qr_img.size

    label_lines = wrap_text(label, width=18)
    subtext_lines = wrap_text(subtext, width=22) if subtext else []

    dummy = Image.new("RGB", (10, 10))
    draw = ImageDraw.Draw(dummy)

    label_height_total = 0
    for line in label_lines:
        _, h = get_text_size(draw, line, TITLE_FONT)
        label_height_total += h + 6

    subtext_height_total = 0
    for line in subtext_lines:
        _, h = get_text_size(draw, line, SUBTEXT_FONT)
        subtext_height_total += h + 4

    card_width = qr_w + CARD_PADDING * 2
    card_height = (
        qr_h
        + CARD_PADDING * 2
        + LABEL_TOP_PADDING
        + label_height_total
        + (SUBTEXT_TOP_PADDING if subtext_lines else 0)
        + subtext_height_total
    )

    card = Image.new("RGB", (card_width, card_height), CARD_BACKGROUND)
    card_draw = ImageDraw.Draw(card)

    card_draw.rounded_rectangle(
        (0, 0, card_width - 1, card_height - 1),
        radius=CARD_CORNER_RADIUS,
        fill=CARD_BACKGROUND,
        outline=CARD_BORDER_COLOR,
        width=CARD_BORDER_WIDTH
    )

    qr_x = (card_width - qr_w) // 2
    qr_y = CARD_PADDING
    card.paste(qr_img, (qr_x, qr_y))

    current_y = qr_y + qr_h + LABEL_TOP_PADDING

    for line in label_lines:
        text_w, text_h = get_text_size(card_draw, line, TITLE_FONT)
        text_x = (card_width - text_w) // 2
        card_draw.text((text_x, current_y), line, fill=TEXT_COLOR, font=TITLE_FONT)
        current_y += text_h + 6

    if subtext_lines:
        current_y += SUBTEXT_TOP_PADDING

        for line in subtext_lines:
            text_w, text_h = get_text_size(card_draw, line, SUBTEXT_FONT)
            text_x = (card_width - text_w) // 2
            card_draw.text((text_x, current_y), line, fill=TEXT_COLOR, font=SUBTEXT_FONT)
            current_y += text_h + 4

    return card


# =========================================================
# GUI APP
# =========================================================

class FancyPantsQRGui:
    def __init__(self, root):
        self.root = root
        self.root.title("Fancy Pants QR Code Generator v2.0")
        self.root.geometry("700x600")

        self.logo_path = tk.StringVar(value="./image_path")
        self.output_folder = tk.StringVar(value="./output_folder")

        self.label_var = tk.StringVar(value="Label Name A\nLabel Name B (Optional)")
        self.filename_var = tk.StringVar(value="File Name")
        self.url_var = tk.StringVar(value="https://URL-Path-Here")
        self.subtext_var = tk.StringVar(value="Subtext A\nSubtext B (Optional)")

        self.build_ui()

    def build_ui(self):
        # Main canvas + scrollbar setup
        outer_frame = tk.Frame(self.root)
        outer_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(outer_frame)
        scrollbar = tk.Scrollbar(outer_frame, orient="vertical", command=canvas.yview)

        self.scrollable_frame = tk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda event: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas_window = canvas.create_window(
            (0, 0),
            window=self.scrollable_frame,
            anchor="nw"
        )

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Make inner frame resize with window width
        def resize_scrollable_frame(event):
            canvas.itemconfig(canvas_window, width=event.width)

        canvas.bind("<Configure>", resize_scrollable_frame)

        # Mouse wheel support, Mac + Windows
        def on_mousewheel(event):
            if event.num == 4:
                canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                canvas.yview_scroll(1, "units")
            else:
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", on_mousewheel)   # Windows / Mac
        canvas.bind_all("<Button-4>", on_mousewheel)     # Linux scroll up
        canvas.bind_all("<Button-5>", on_mousewheel)     # Linux scroll down

        container = tk.Frame(self.scrollable_frame, padx=20, pady=20)
        container.pack(fill="both", expand=True)

        title = tk.Label(
            container,
            text="Fancy Pants QR Code Generator",
            font=("Arial", 18, "bold")
        )
        title.pack(anchor="w", pady=(0, 15))

        self.add_text_area(container, "Label", self.label_var, height=3)
        self.add_entry(container, "File Name", self.filename_var)
        self.add_entry(container, "URL", self.url_var)
        self.add_text_area(container, "Subtext", self.subtext_var, height=3)

        logo_frame = tk.LabelFrame(container, text="Optional Logo", padx=10, pady=10)
        logo_frame.pack(fill="x", pady=8)

        tk.Entry(logo_frame, textvariable=self.logo_path).pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 8)
        )
        tk.Button(logo_frame, text="Browse Logo", command=self.browse_logo).pack(side="left")
        tk.Button(logo_frame, text="Clear", command=self.clear_logo).pack(side="left", padx=(8, 0))

        output_frame = tk.LabelFrame(container, text="Output Folder", padx=10, pady=10)
        output_frame.pack(fill="x", pady=8)

        tk.Entry(output_frame, textvariable=self.output_folder).pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 8)
        )
        tk.Button(output_frame, text="Browse Output", command=self.browse_output_folder).pack(side="left")

        button_frame = tk.Frame(container)
        button_frame.pack(fill="x", pady=20)

        tk.Button(
            button_frame,
            text="Generate QR Card",
            command=self.generate_qr,
            height=2,
            bg="#222222",
            fg="#FFFFFF"
        ).pack(fill="x")

        help_text = (
            "Tip: Use \\n in the label or subtext to force a new line.\n"
            "Example: Label A\\nLabel B"
        )

        tk.Label(container, text=help_text, justify="left", fg="#FFFFFF").pack(
            anchor="w",
            pady=(10, 0)
        )

    def add_entry(self, parent, label, variable):
        frame = tk.LabelFrame(parent, text=label, padx=10, pady=10)
        frame.pack(fill="x", pady=8)

        entry = tk.Entry(frame, textvariable=variable)
        entry.pack(fill="x")

    def add_text_area(self, parent, label, variable, height=3):
        frame = tk.LabelFrame(parent, text=label, padx=10, pady=10)
        frame.pack(fill="x", pady=8)

        text_box = tk.Text(frame, height=height, wrap="word")
        text_box.insert("1.0", variable.get())
        text_box.pack(fill="x")

        def update_variable(event=None):
            variable.set(text_box.get("1.0", "end-1c"))

        text_box.bind("<KeyRelease>", update_variable)

    def browse_logo(self):
        file_path = filedialog.askopenfilename(
            title="Select Logo Image",
            filetypes=[
                ("Image Files", "*.png *.jpg *.jpeg *.webp"),
                ("PNG Files", "*.png"),
                ("All Files", "*.*")
            ]
        )

        if file_path:
            self.logo_path.set(file_path)

    def clear_logo(self):
        self.logo_path.set("")

    def browse_output_folder(self):
        folder_path = filedialog.askdirectory(title="Select Output Folder")

        if folder_path:
            self.output_folder.set(folder_path)

    def generate_qr(self):
        label = self.label_var.get().strip()
        filename = self.filename_var.get().strip()
        url = self.url_var.get().strip()
        subtext = self.subtext_var.get().strip()
        logo = self.logo_path.get().strip()
        output_folder = self.output_folder.get().strip()

        if not output_folder or output_folder == "Select Output Folder":
            output_folder = os.path.join(os.getcwd(), "portfolio_qr_output")

        if not label:
            messagebox.showerror("Missing Label", "Please enter a label.")
            return

        if not filename:
            messagebox.showerror("Missing File Name", "Please enter a file name.")
            return

        if not url:
            messagebox.showerror("Missing URL", "Please enter a URL.")
            return

        if not url.startswith("http://") and not url.startswith("https://"):
            messagebox.showerror("Invalid URL", "URL must start with http:// or https://")
            return

        try:
            os.makedirs(output_folder, exist_ok=True)

            safe_filename = filename.replace(" ", "_").replace("/", "_").replace("\\", "_")
            output_path = os.path.join(output_folder, f"{safe_filename}.png")

            card = create_qr_card(
                label=label,
                subtext=subtext,
                url=url,
                logo_path=logo if logo else None
            )

            card.save(output_path)

            messagebox.showinfo(
                "QR Code Created",
                f"Saved QR card:\n{output_path}"
            )

            try:
                card.show()
            except Exception:
                pass

        except Exception as e:
            messagebox.showerror("Error", f"Could not generate QR code:\n{e}")


# =========================================================
# MAIN
# =========================================================

def main():
    root = tk.Tk()
    app = FancyPantsQRGui(root)
    root.mainloop()


if __name__ == "__main__":
    main()
