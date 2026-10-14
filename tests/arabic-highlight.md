# A36-A39 Arabic Highlight Regression

This fix is deliberately limited to A36-A39 in the 1.4.4 teacher and textbook/student apps. Earlier units, lesson data, audio files, and review feedback are unchanged.

- Arabic color emphasis uses CSS Custom Highlight ranges on unbroken text nodes. No ZWJ characters are added, and font weight does not change inside a word.
- Whole-word boxes remain boxes. A box cutting through a word becomes a paint-only background and underline, so padding and borders cannot interrupt joining.
- Browsers without the Highlight API emphasize the complete affected word with inherited font metrics. This sacrifices partial-word coloring to preserve correct Arabic.
- Highlight ranges are rebuilt after slide changes and before printing. Detached ranges are replaced, not accumulated.

Run `node tests/check-arabic-highlight.mjs`. The legacy fixture was captured from main at `e42c5a132d4ab392bb2706de8c45fcb4d9e77638` and verifies that old-unit parser output is byte-for-byte unchanged.

Serve the repo and open `tests/arabic-highlight.html` and `tests/arabic-highlight.html?fallback=1`. Both must pass. The page checks text preservation and shaping widths in Noto Sans Arabic and Dongol, including lam-alif, harakat-only emphasis, tanwin, shadda, hamza, nested markers, and mixed Korean/Arabic.

Manually inspect A36-A39 patterns, repertories, and drills on desktop and mobile. No sheet statuses or audio review checkboxes should be changed during verification.

References: [W3C inline-boundary shaping](https://www.w3.org/TR/css-text-3/#boundary-shaping), [CSS Custom Highlight API](https://www.w3.org/TR/css-highlight-api-1/).
