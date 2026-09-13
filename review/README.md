# ATA 1.4.4 public audio review

`ata144-a21-a35-nass.json` is the public manifest used by the GitHub Pages audio-review link.
Its audio files live under the isolated GCS review prefix, not the production app audio path.

Shared reviewer feedback is read with:

```sh
python3 tools/fetch_144_review_feedback.py
```

The local API URL and review key are stored in the ignored `.review-feedback-144.env` file.
