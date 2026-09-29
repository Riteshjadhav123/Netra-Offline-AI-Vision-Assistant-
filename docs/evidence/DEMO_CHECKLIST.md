# Netra Demonstration & Video Checklist

Use this checklist to record the 60-90 second competition video and capture submission screenshots.

---

## 📹 Video Setup (60-90 Seconds)

- [ ] **Step 1: Offline Setup Proof**
  - Show the Windows system tray with **Wi-Fi / Airplane Mode explicitly turned OFF**.
  - Show the Netra application launching via `run.bat` or `python main.py`.

- [ ] **Step 2: Object Detection Demo**
  - Hold a physical object (e.g. `bottle` or `laptop`) in front of the camera.
  - Press `SPACE`.
  - Show the bounding box and green tag appear on screen.
  - Verify Netra speaks: *"I see a bottle."*

- [ ] **Step 3: Text Reading (OCR) Demo**
  - Hold a printed sign, book cover, or prescription bottle with text (e.g., *"EXPIRY 2027"*) in front of the camera.
  - Press `SPACE`.
  - Show the read text appear on the dashboard panel under `Reads:`.
  - Verify Netra speaks: *"The visible text reads: 'EXPIRY 2027'."*

- [ ] **Step 4: Combined Scene & Text Demo**
  - Hold a book and bottle together in front of the camera.
  - Press `SPACE`.
  - Verify Netra speaks: *"I see a bottle and a book. The visible text reads..."*

- [ ] **Step 5: Smooth Quit**
  - Press `Q` to close the application cleanly.

---

## 📸 Screenshots Required for Submission

1. `01_app_startup.png`: Netra high-contrast UI immediately after launch.
2. `02_object_detection.png`: Camera view showing bounding box around a detected object.
3. `03_ocr_text_reading.png`: Dashboard panel displaying recognized printed text.
4. `04_spoken_response.png`: Spoken answer line rendered on the dashboard.
5. `05_environment_verification.png`: Terminal output from `python scripts/verify_environment.py`.
