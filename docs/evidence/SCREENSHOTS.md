# Netra UI Screenshots Guide

## Dashboard Layout

The Netra user interface is rendered directly on the OpenCV window with a dark high-contrast dashboard panel beneath the camera feed.

### Panel Layout Blueprint

```
+-------------------------------------------------------------------+
|                                                                   |
|                      LIVE CAMERA FEED                             |
|       [ Green Bounding Box: bottle (94%) ]                        |
|                                                                   |
+-------------------------------------------------------------------+
| NETRA AI ASSISTANT | Status: Ready — Press SPACE to look & speak  |
| Engine Provider: CPUExecutionProvider (Detection: 50.7ms)        |
| Sees: bottle, book                                                |
| Reads: EXPIRY 2027                                                |
| Says: I see a bottle and a book. The visible text reads: 'EXPIRY' |
+-------------------------------------------------------------------+
```

## Screen Captures List

1. **`01_startup.png`**: Netra ready state.
2. **`02_detection.png`**: Bounding box visualization on detected objects.
3. **`03_ocr.png`**: Text recognition on printed labels.
4. **`04_verification.png`**: Verification script execution (`verify_environment.py`).
