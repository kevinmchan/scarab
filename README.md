# Scarab

A social deduction game set at a 1926 Egyptian tomb excavation. Seven members of the
expedition break the seal; two of them are Cultists. Share a link, take a place, and
argue about who to send into the desert.

Empty places are filled by characters the game plays — an epigrapher, an illustrator,
a camp guard, a financier, a surveyor, and a foreman, each with their own voice, their
own read on the evidence, and their own way of lying when they turn out to be marked.

## Playing

Open the site. You get a dig code and a link — send the link to whoever is playing.
Everyone takes a place, someone breaks the seal, and the game runs from there.

**Whoever starts the game keeps time for it**, so that person should leave their tab
open. If they close it, everyone else sees an offer to take over.

## Roles

| Role | Night | Wins when |
| --- | --- | --- |
| **Cultist** ×2 | Together, take one member | Cultists equal everyone else left alive |
| **Scribe** | Divine one member — are they marked? | Both Cultists are cast out |
| **Medjai** | Ward one member against being taken | Both Cultists are cast out |
| **Digger** ×3 | — | Both Cultists are cast out |

## How it is built

One self-contained HTML file, no framework, no build step at runtime.

State is an **append-only event log**. Every player's browser replays the whole log to
derive identical game state, so there is no authoritative server — only the log. The
view whose player started the game runs the engine (phase changes, the AI characters'
decisions) and commits the results as events; every other view just replays.

That log travels one of two ways, chosen at boot:

- **Self-hosted** (this site): rows in Postgres, polled for new events. Row-level
  security permits appending to a dig and reading it, and nothing else, so no client
  can rewrite history.
- **As a Claude artifact**: the artifact runtime's own sync, no backend at all.

Hidden information is hidden from the *log*, not just the interface — a night action
is stored as one opaque blob rather than `seat` + `action`, which would otherwise let
anyone reading the raw data see who is a Cultist. For the same reason a Cultist's
deflection is recorded publicly under a neutral label.

### Building

```bash
python3 build.py
```

Reads `scarab.src.html` plus `content/`, writes `index.html` (deployed) and
`scarab.html` (a bare fragment for publishing as a Claude artifact). Edit
`scarab.src.html`, never the built files.

`patch_content.py` rewrites dialogue lines that referred to a target as "he" or "the
man" — characters are dealt to places at random and targets include human players, so
gendered phrasing misgenders whoever it lands on. Re-run it after regenerating
`content/personas.json`.

## Putting it on scarab.quest

The site is live at <https://kevinmchan.github.io/scarab/>. To move it to the custom
domain, buy `scarab.quest`, add these records at the registrar, then run
`./setup-domain.sh`:

| Type | Name | Value |
| --- | --- | --- |
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| CNAME | www | kevinmchan.github.io. |

The script refuses to run until DNS actually points at GitHub, because setting the
custom domain early redirects the working URL to a domain that isn't answering yet.
Share links are built from whatever address the page is served on, so they follow the
domain automatically.
