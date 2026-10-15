# Alphabet Baseline Layout Regression

The reported alphabet `ptn013` belongs to A05, not A33. At a 1280px viewport,
the six intrinsic grid columns had unequal widths (175, 175, 182, 182, 116,
116px). Their content overflowed the RTL grid to the left. Scaling its client
box did not center that overflowing content.

The teacher renderer now measures the widest glyph group or label, allocates
equal-width tracks, centers their natural-width box, and scales it to the
available width. It recalculates on font load and resize. Normal sentence and
nass renderers are unchanged.

## Browser Checks

1. Open `ata144_teacher/ata144_teacher.html?unit=A05&slide=1` at 1280px.
   Verify all six letters, connecting forms and pronunciation labels align.
   The grid and wrapper centers should differ by less than 1px.
2. Repeat at 390px; no glyph should overlap its neighboring column or spill
   outside the wrapper. Resize back and confirm the layout recalculates.
3. Open A33's first and third pattern slides; sentence alignment must remain
   centered and the Arabic text must stay joined.
4. Open A32/A33 in the student textbook and confirm the pattern/repertory
   links and the 49/35 drill counts after the separate Sheet revision.

Verified 2026-10-15 with the in-app browser: desktop grid center 640.10px,
wrapper center 640px; six equal 182.17px natural tracks. Mobile alphabet
columns remain within the wrapper. All inline teacher scripts parse.

The Sheet revision preserves its ARRAYFORMULA columns, all A32/A33 nass rows
and audio IDs. Teaching-sentence audio uses new note-derived filenames.
