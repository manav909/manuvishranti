# manuvishranti.com

## What this repo is
A static site. One self-contained HTML file per experience, no build step, no server.
Each experience lives in its own folder, so the root stays free for a home page later.

Live experience: **लंका की खोज** at `/lanka_ki_khoj`, a Hindi discovery game built on the Sundar Kand,
covering 19 texts, 25 places, 63 forms, 77 hidden findings, all with citations.

## Stack
- Plain HTML + CSS + SVG + vanilla JS in a single file
- No dependencies, no bundler. Google Fonts is the only outbound request
- Player progress lives in browser localStorage, keyed to the domain

## Deploy
- Host: Vercel (static). Framework preset: Other. Build command: none. Output directory: repo root
- Domain: manuvishranti.com (apex + www)
- The game answers at manuvishranti.com/lanka_ki_khoj
- Publish = push to `main`. Vercel rebuilds automatically

## Files
- `lanka_ki_khoj/index.html` — the game, complete and standalone
- `PROJECT_BRIEF.md` — this file
- root `index.html` — not made yet, kept free for the home page

## Working rules carried over
- Complete files only, never patches
- No em dashes or en dashes anywhere, Hindi or English
- Verify before publishing: `node --check` on the extracted script, plus the test suite
- Commit messages: plain ASCII, single quotes
- Stage finals in outputs, then one paste-able command

## Test suite (run in the build container, not in the repo)
26 check files covering: whole-project data integrity, language, camera, map thinning,
panels, scroll anchoring, story cards, gift boxes, the woven scroll, the thread of the story,
progress card, titles, adhikar gates, parakh questions, prahar gifts, repeat visits, layout.

## Next steps parked
- Fourth night: विलंका की रात as a playable part (currently a purchasable reading)
- Side by side reading of two texts on one moment
- One original line per citation in its own script with a plain translation
