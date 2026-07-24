# Private photo-library ingestion

This pipeline turns an original-quality Google Photos album ZIP into a private, searchable working catalog without extracting the whole archive or committing the originals to Git.

## Safety boundary

- Keep the source ZIP and generated catalog outside the repository.
- The private catalog may contain exact EXIF location and OCR text. Do not publish or commit it.
- The review catalog omits exact GPS coordinates, but remains private because OCR and bystander information can still be sensitive.
- `identity_clues` are evidence notes, not face-recognition results. A name must come from visible text, supplied event context, or another attributable source and remain tentative until reviewed.
- Every asset starts as `unreviewed`. WordPress upload and public-site use require explicit asset approval.

## Run

```bash
python3 scripts/photo-library/catalog_album.py \
  "/path/to/KK PHotos.zip" \
  --library-root "$HOME/Pictures/KK Media Library/Google Photos/KK PHotos" \
  --title "KK PHotos" \
  --ocr
```

The script streams each ZIP member through SHA-256, extracts only one temporary file at a time for EXIF/OCR/thumbnail work, and deduplicates by content hash on later runs. It writes:

- `private/manifest.json` — archive checksum and run counts
- `private/catalog.jsonl` — full private metadata, OCR, and source occurrences
- `review/index.html` — local filterable contact catalog
- `review/catalog.{json,csv}` — GPS-redacted review data
- `review/annotations.jsonl` — working captions, event names, identity clues, uses, and approval state
- `review/sheets/` — compact visual sheets for computer-vision review

Dependencies are deliberately local and small: ExifTool for metadata, Tesseract for optional OCR, and Pillow (with macOS `sips` as the thumbnail fallback). Missing optional tools degrade to a hash/date catalog rather than exposing data to a cloud service.

The Google Photos album is auto-updating. Preserve each downloaded ZIP as a dated source snapshot; rerunning the catalog against a newer snapshot adds only new SHA-256 assets and records duplicate source occurrences.
