# My Fancy Pants QR Code Generator:
A Python desktop GUI tool for creating branded QR code cards for portfolios, resumes, GitHub pages, and project links.

[Demo:](https://khucker3d.carbonmade.com/projects/7254185#2)

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

## [How To]():

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

## Future Improvement Ideas:
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

### Security Notes:
* This project is intended for learning, personal security practice, and portfolio demonstration.
* For real credential storage, use a trusted password manager.
