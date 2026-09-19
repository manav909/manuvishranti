# manuvishranti.com

## What this repo is
A static site. One self-contained HTML file per experience, no build step, no server.
Each experience lives in its own folder, so the root stays free for a home page later.

Live experience: **लंका की खोज** at `/lanka_ki_khoj`, a Hindi discovery game built on the Sundar Kand,
covering 41 tellings of the Sundar Kand from India and beyond, 47 moments, 153 hidden findings,
35 places, 24 people, 20 boons and weapons, 43 detours inside tellings, 10 side by side differences
and 4 playable nights, all with citations.

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

## The unbreakable rule
Whenever anything is added, removed or renamed - a scene, a place, a character, a find, a line, a citation -
every reference to it must be updated in the same edit. `linktest.js` enforces this and must be run every time.
It walks every cross reference in both directions: moments to nights, places to pictures, finds to texts,
people to finds, badges to their meters, differences to their rows, the thread to its moments,
shut kathas to their conditions, nights to the night or katha they wait on, texts to their homes,
and it fails on any orphan, any dangling name, and any duplicate key.

## Test suite (run in the build container, not in the repo)
31 check files covering: whole-project data integrity, language, camera, map thinning,
panels, scroll anchoring, story cards, gift boxes, the woven scroll, the thread of the story,
progress card, titles, adhikar gates, parakh questions, prahar gifts, repeat visits, layout.

## Next steps parked
- Fourth night: विलंका की रात as a playable part (currently a purchasable reading)
- Side by side reading of two texts on one moment
- One original line per citation in its own script with a plain translation
