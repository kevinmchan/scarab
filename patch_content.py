#!/usr/bin/env python3
"""De-gender template lines that refer to a slot-filled person.

Personas are dealt to seats at random and targets include human players, so a
line like "how the man stands" misgenders whoever it lands on. Lines where the
gendered word means the speaker or the workmen are left alone.
Rerun after regenerating personas.json.
"""
import json, pathlib, sys

SCRATCH = pathlib.Path(__file__).parent / 'content'

FIXES = {
 'hollis': {'react_death': [("{dead} is dead and the sand around him is swept. someone tidied.",
                             "{dead} is dead and the sand around the body is swept. someone tidied.")]},
 'brennan': {
   'accuse': [("Wrong tone, {target}. Innocent men don't sound the way you sound.",
               "Wrong tone, {target}. Innocent people don't sound the way you sound.")],
   'accuse_evidence': [("{evidence}. That's not nerves, {target}. That's a man COVERING.",
                        "{evidence}. That's not nerves, {target}. That's COVERING.")],
   'soft_read': [("{target} sits too quiet for a man with nothing on him. Noted.",
                  "{target} sits too quiet for someone with nothing to hide. Noted.")],
   'doubt_claim': [("Wrong. A real one wouldn't sound so pleased with himself saying it.",
                    "Wrong. A real one wouldn't sound so pleased saying it.")],
   'pressure_quiet': [("You've gone very quiet, {target}. Quiet men make me nervous.",
                       "You've gone very quiet, {target}. Quiet ones make me nervous.")],
   'vote_announce': [("{target}. Out past the torches. I'll walk him to the ridge myself.",
                      "{target}. Out past the torches. I'll walk them to the ridge myself.")],
   'react_eject_crew': [("Wrong. I was wrong, and there's a man in the sand for it.",
                         "Wrong. I was wrong, and there's a body in the sand for it.")],
 },
 'percy': {
   'doubt_claim': [("If {claimant} is telling the truth, he's the unluckiest honest man in Egypt.",
                    "If {claimant} is telling the truth, that's the unluckiest honest soul in Egypt."),
                   ("I'll believe {claimant} the moment the story costs him something.",
                    "I'll believe {claimant} the moment the story costs something.")],
   'pressure_quiet': [("Silence is very comfortable, isn't it, {target}. Nobody votes for a man they've forgotten.",
                       "Silence is very comfortable, isn't it, {target}. Nobody votes for someone they've forgotten."),
                      ("{target} has spent the morning studying his boots. Boots aren't evidence either.",
                       "{target} has spent the morning studying the ground. The ground isn't evidence either.")],
   'react_death': [("{dead}. Good God. He was arguing with me about the water ration on Tuesday.",
                    "{dead}. Good God. We were arguing about the water ration on Tuesday."),
                   ("Cover him properly. Then we talk — about who wanted {dead} quiet.",
                    "Cover the body properly. Then we talk — about who wanted {dead} quiet.")],
   'react_eject_crew': [("We killed a man over a hunch — mine, in part. That will sit with me a while.",
                         "We killed someone over a hunch — mine, in part. That will sit with me a while."),
                        ("I'll pay {ejected}'s family whatever the season owed him. It buys nothing, I know.",
                         "I'll pay {ejected}'s family whatever the season owed. It buys nothing, I know.")],
 },
 'tahir': {
   'accuse': [("{target}. Something wrong in how the man stands.",
               "{target}. Something wrong in how that one stands.")],
   'defend_other': [("Not {target}. I've worked beside the man. Wrong tree.",
                     "Not {target}. I've worked beside them. Wrong tree."),
                    ("{target} carried the plaster up alone. I watched him do it.",
                     "{target} carried the plaster up alone. I watched it done.")],
   'soft_read': [("I'd watch {target} today. Wouldn't cast him out yet.",
                  "I'd watch {target} today. Wouldn't cast them out yet.")],
   'doubt_claim': [("{claimant} finds his role the moment the rope comes out. Convenient.",
                    "{claimant} finds a role the moment the rope comes out. Convenient."),
                   ("Every dig has a man who suddenly matters. Today it's {claimant}.",
                    "Every dig has someone who suddenly matters. Today it's {claimant}.")],
   'deflect': [("Ask {target} what he told the workmen last night. Then come back to me.",
                "Ask {target} what was said to the workmen last night. Then come back to me."),
               ("There's a man in this tent who's said nothing worth hearing. {target}.",
                "There's someone in this tent who's said nothing worth hearing. {target}.")],
   'pressure_quiet': [("Quiet men make me nervous, {target}.",
                       "Quiet ones make me nervous, {target}.")],
   'react_death': [("{dead}. Found him myself. The men won't go near the shaft now.",
                    "{dead}. Found the body myself. The men won't go near the shaft now."),
                   ("Second time in my life I've seen a man like that. Never gets ordinary.",
                    "Second time in my life I've seen a body like that. Never gets ordinary."),
                   ("I told {dead} to sleep near the fire. He didn't listen.",
                    "I told {dead} to sleep near the fire. No one listens.")],
 },
}

personas = json.loads((SCRATCH / 'personas.json').read_text())
by_id = {p['personaId']: p for p in personas}
applied = missing = 0
for pid, intents in FIXES.items():
    for intent, pairs in intents.items():
        arr = by_id[pid]['templates'][intent]
        for old, new in pairs:
            if old in arr:
                arr[arr.index(old)] = new
                applied += 1
            elif new in arr:
                applied += 1  # already patched
            else:
                print(f'MISSING {pid}/{intent}: {old[:60]}', file=sys.stderr)
                missing += 1

(SCRATCH / 'personas.json').write_text(json.dumps(personas, indent=0))
print(f'de-gendered {applied} lines' + (f', {missing} MISSING' if missing else ''))
sys.exit(1 if missing else 0)
