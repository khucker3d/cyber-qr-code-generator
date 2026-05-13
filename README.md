# My Fancy Pants QR Code Generator:
A Python desktop GUI tool for creating branded QR code cards for portfolios, resumes, GitHub pages, and project links.

[Demo:](https://my.carbonmade.com/portfolio/projects/7254185)

<img width="576" height="622" alt="Screenshot 2026-05-13 at 11 30 45" src="https://github.com/user-attachments/assets/308608b9-8952-4f47-bc21-b9ec641d6153"/>

## Features:
* Generate QR code cards from custom URLs
* Add custom labels
* Add custom file names
* Add custom subtext
* Optional center logo support
* Supports manual line breaks in labels and subtext
* Exports QR cards as PNG files
* User-selectable output folder
* Scrollable Tkinter UI
* Mac and Windows friendly
* QR-safe high contrast design
* Clean card layout for resumes, websites, GitHub, and portfolio use

### Use Cases:
* Resume QR codes
* Portfolio QR codes
* GitHub profile links
* Project page links
* Contact cards
* Career hub links
* Printed handouts
* Website image assets
* Important Notes

## Tech Stack
* Python
* Tkinter
* qrcode
* Pillow
* os
* textwrap

## Installation:
1. Download `fancy_pants_qr_gui.py` to your preferred local location.
2. Install required packages:
   * Mac Terminal: `pip3 install "qrcode[pil]`
   * Windows PowerShell: `py -m pip install "qrcode[pil]`

3. Run the script:
   * Mac Terminal: `python3 fancy_pants_qr_gui.py`
   * Windows PowerShell: `py fancy_pants_qr_gui.py`

## How to Use:
1. Open the app
2. Enter a label
3. Enter a file name
4. Enter the destination URL
5. Enter optional subtext
6. Select an optional logo image
7. Choose an output folder
8. Click Generate QR Card
Results: The generated QR card will be saved as a PNG file.


## Important: 
* QR codes should be tested before publishing.
* Use trusted URLs only.
* Avoid linking directly to files if the mobile preview experience is unreliable.

### Security Notes:
* QR codes hide the destination URL from the viewer until scanned.
* Malicious QR codes can be used for phishing.
* Public QR codes should point to trusted domains.
* Avoid URL shorteners for professional or portfolio use.
* Test QR codes on both desktop and mobile devices.

### Limitations:
* Does not verify whether a URL is live.
* Does not detect malicious URLs.
* Does not create hosted landing pages.
* Logo placement may affect scan reliability if the logo is too large.
* Generated files are static PNG images.

### Future Improvement Ideas:
* Multiple QR item list inside the GUI
* Combined portfolio sheet export from GUI
* Color picker support
* Built-in QR scan reliability checker
* URL validation preview
* Drag and drop logo support
* Save and load QR presets
* Export PDF contact sheet
* Packaged Mac and Windows app builds

## License:
MIT License
