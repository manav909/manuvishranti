# manuvishranti.com

## What this repo is
A static site. One self-contained HTML file per experience, no build step, no server.
Each experience lives in its own folder, so the root stays free for a home page later.

Live experience: **लंका की खोज** at `/lanka_ki_khoj`, a Hindi discovery game built on the Sundar Kand,
covering 41 tellings from India and beyond, 6 playable nights, 108 moments, 307 hidden findings,
96 places, 53 detours inside tellings, 38 people, 34 boons and weapons, 12 stories told inside the story,
14 side by side differences, 22 badges, 32 titles and 15 original lines in their own script, all with citations.

## How a night runs
- Each night is four prahars, and each prahar splits into two ghadis
- The first ghadi belongs to the katha: the places the story itself passes through, in the order the
  text gives them, one after another, free of the visit budget. The thread can never be missed
- The second ghadi is the player's: the places running at the same time, filtered to the road their
  role walks, with the rest one tap away
- 41 named beats make up the thread. `ghaditest.js` enforces all of this

## Roles
- Eight roles: jigyasu, yatri, kathapremi, balak, yoddha (open from the start), shastri, sadhak, raja
  (earned). Picking one is the first screen, and the role settles once a night begins
- A role carries its own places no one else can see, its own people, its own detour, its own
  collectible, its own badge, its own two titles, its own eye at every kind of place, its own
  reckoning at dawn, its own leaning in the questions, and its own colour across the whole game
- It also carries: an aim for every night, a parting line for every rasa, a closing line for the
  morning, a rank ladder of seven, a name for the player, a pointer planted on its own places,
  a first night the list puts on top, the page the notebook opens on, and the register the game
  speaks in (शास्त्री, साधक and राजा are addressed as आप, the rest as तुम)
- The shape of a moment changes too: the warrior gets a reckoning, the scholar a citation, the
  katha lover the other tellings, the child something to enjoy, the king the decision, the seeker
  a pause, the traveller what to look at
- Around 240 lines are written for the roles: an aim for each night, a parting line for each rasa, a
  closing line for the morning, a rank ladder of seven, and five things the role simply knows, each
  waiting at a different kind of place, folded away and said once
- 36 of the 96 places belong to one role alone, and every role owns at least four, including at least
  one in the later three nights
- Every role keeps its own journey on the device: switching roles puts one away and picks the other up
  exactly where it was left, and leaving one journey leaves the rest alone
- The katha ghadi never bends to the role. `roletest.js` enforces all of it

## The look
- Time of day drives everything: the map light, the panel palette, the motes in the air, the rim light
  on the people in the scenes. Each of the three extra nights also has its own colour world
- Depth everywhere: shadows under pins and cards, a haze and a vignette inside every scene, a black
  foreground layer that drifts against the scene, a grain over the map
- Motion, all of it behind `prefers-reduced-motion` and behind a "हरकत कम" switch the player controls:
  a curtain at the turn of the hour, a jolt on arrival, sparks in fire scenes, wind over the water,
  smoke over the burning city, a shimmering sea, city lights that wake at night, streets that appear
  on zoom. `feeltest.js` enforces the whole layer

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
- `lanka_ki_khoj/index.html`: the game, complete and standalone
- `PROJECT_BRIEF.md`: this file
- root `index.html`: not made yet, kept free for the home page

## Working rules carried over
- Complete files only, never patches
- No em dashes or en dashes anywhere, Hindi or English
- Verify before publishing: `node --check` on the extracted script, plus the test suite
- Commit messages: plain ASCII, single quotes
- Stage finals in outputs, then one paste-able command

## The unbreakable rule
Whenever anything is added, removed or renamed - a scene, a place, a character, a find, a line, a citation,
every reference to it must be updated in the same edit. `linktest.js` enforces this and must be run every time.
It walks every cross reference in both directions: moments to nights, places to pictures, finds to texts,
people to finds, badges to their meters, differences to their rows, the thread to its moments,
shut kathas to their conditions, nights to the night or katha they wait on, texts to their homes,
and it fails on any orphan, any dangling name, and any duplicate key.

## Test suite (run in the build container, not in the repo)
39 check files covering: whole-project data integrity, language, camera, map thinning, panels,
scroll anchoring, story cards, gift boxes, the woven scroll, the thread of the story, progress card,
titles, adhikar gates, parakh questions, prahar gifts, repeat visits, layout, the two ghadis,
the eight roles, the whole visual layer, the colour contrast of every palette in every hour, and a
check that no line in the game is said twice anywhere, in any role or between two roles.

## Next steps parked
- More original lines in their own script with a plain translation (15 so far)
- Player accounts, so the per role journeys follow the player instead of living on one device
- Keep filling the thinnest tellings, one pass at a time
