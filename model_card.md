# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

VibeFinder 1.0 suggests up to five songs from a small catalog based on a user's preferred genre, mood, energy level, valence, and acoustic preference. It is designed for **classroom exploration** — to illustrate how content-based filtering works — and should **not** be used as a production music recommender. It assumes the user can describe their preferences numerically and that a single static profile captures their mood at any given moment, which is rarely true for real listeners.

---

## 3. How the Model Works

The system compares each song's attributes against what the user says they like, then adds up a relevance "score" for every track:

- **Genre match** earns the most points (2.0). If the song's genre matches the user's favourite genre exactly, it gets full points; otherwise it gets nothing.
- **Mood match** is second (1.5 points). Same idea — exact string match.
- **Energy closeness** rewards songs that are near the user's target energy level. A song that is exactly the right energy earns 1.0 point; every step away from the target reduces that score smoothly down to 0.
- **Valence closeness** works the same way but counts for half as much (up to 0.5 points). Valence measures musical brightness or positivity.
- **Acoustic bonus** adds 0.5 points if the user likes acoustic music and the song is predominantly acoustic.

All songs are scored, then sorted from highest to lowest. The top five are returned as recommendations along with a plain-English explanation of each score.

---

## 4. Data

The catalog (`data/songs.csv`) contains **18 songs** across a variety of genres: pop, lofi, rock, jazz, ambient, hip-hop, country, classical, metal, reggae, R&B, EDM, synthwave, indie pop, and folk. Each song has seven numerical or categorical attributes: genre, mood, energy (0–1), tempo in BPM, valence (0–1), danceability (0–1), and acousticness (0–1).

Eight additional songs were added beyond the original ten starter tracks to improve genre diversity. Even so, the dataset is tiny and reflects a particular stylistic snapshot — predominantly Western popular music genres. Listeners whose tastes centre on non-Western music, niche subgenres, or moods not already in the catalog will receive poor recommendations.

---

## 5. Strengths

- **Transparent**: every recommendation comes with a plain-English explanation of exactly why it scored the way it did.
- **Works for new users**: because the system only needs the user's stated preferences (not listening history), it gives reasonable results from the very first query.
- **Handles clear tastes well**: profiles with a well-represented genre in the catalog (e.g., "lofi/chill") consistently receive results that match musical intuition — the two lofi tracks topped every list for the Chill Lofi Listener profile.
- **Continuous energy scoring** means near-misses still earn partial credit, so the system never completely ignores an otherwise good song just because the energy is slightly off.

---

## 6. Limitations and Bias

**Genre dominance and filter bubbles.** Genre is worth 2.0 points — nearly 36 % of the maximum possible score of 5.5. When the catalog contains more songs in one genre (e.g., three lofi tracks but only one jazz track), users whose favourite genre is lofi will always be served lofi content, regardless of what mood or energy level they want. Over time this creates a feedback loop: users only see one genre, so they never discover others.

**Vocabulary mismatch for moods.** Mood is compared as a plain string. A user who prefers "focused" will score 0 mood points against a song tagged "chill," even though those states are musically adjacent. The system has no understanding of semantic similarity between mood labels.

**Small, culturally narrow catalog.** Eighteen songs cannot represent global musical taste. Genres like Afrobeat, K-pop, bossa nova, or bhangra are entirely absent. A user whose music culture is underrepresented in the CSV will receive recommendations that may feel completely wrong.

**Binary acoustic preference.** `likes_acoustic` is a true/false flag. Real listeners usually prefer acoustic textures in some contexts (studying, winding down) but not others (working out). A single boolean cannot capture this nuance.

**Adversarial profiles expose scoring gaps.** A user who wants high energy but is tagged "ambient/sad" (conflicting preferences) will see genre match drive the result — they get Spacewalk Thoughts (ambient, chill, low energy) simply because genre earns 2.0 points while the high-energy preference only partially compensates through the energy-proximity term.

---

## 7. Evaluation

Four user profiles were tested:

| Profile | Top result | Matched intuition? |
|---|---|---|
| High-Energy Pop Fan (genre: pop, mood: happy, energy: 0.85) | Sunrise City (score 4.95) | ✅ Yes — genre + mood + energy all aligned |
| Chill Lofi Listener (genre: lofi, mood: chill, energy: 0.40, acoustic: True) | Midnight Coding (score 5.47) | ✅ Yes — two lofi tracks dominated; acoustic bonus helped |
| Intense Rock Head (genre: rock, mood: intense, energy: 0.92) | Storm Runner (score 4.98) | ✅ Yes — the only rock track in the catalog was the clear winner |
| Adversarial (genre: ambient, mood: sad, energy: 0.90, acoustic: True) | Spacewalk Thoughts (score 3.15) | ⚠️ Partly — genre matched, but the high-energy desire was not served |

The adversarial profile revealed the biggest weakness: when a user's genre and energy preferences conflict, genre always wins because of its higher weight. The top recommendation (an ambient, low-energy track) was the opposite of what the user's energy preference asked for.

A weight-shift experiment was also run mentally: doubling the energy weight and halving the genre weight would help the adversarial case but would hurt well-defined profiles like "Intense Rock Head" where only one rock song exists in the catalog.

---

## 8. Future Work

1. **Semantic mood similarity** — replace exact string matching with a small lookup table (or embedding model) that knows "focused" and "chill" are closer to each other than "chill" and "intense."
2. **Diversity penalty** — after scoring, penalise songs from an artist or genre that is already represented in the top results, so the recommended list spans more of the catalog.
3. **Larger, more diverse catalog** — adding hundreds of songs across non-Western genres, sub-genres, and niche moods would make the recommender useful to a broader range of listeners and reduce genre-dominance bias.
4. **Context-aware profiles** — instead of one static profile, allow users to specify different preferences for different activities (working out, studying, relaxing), and let the system pick the right profile automatically based on time of day or session length.

---

## 9. Personal Reflection

Building VibeFinder 1.0 made it clear how much a recommendation system's behaviour is shaped by **how you weight features** rather than by any clever algorithm. Adjusting the genre weight from 2.0 to 0.5 would fundamentally change which songs surface — yet that choice is largely arbitrary at this scale, since there is no feedback loop to tell the system whether users actually liked what it suggested.

The most surprising discovery was how quickly even a tiny catalog creates a filter bubble. With 18 songs and a 2.0-point genre bonus, a pop fan will see pop songs in every single recommendation slot, regardless of their energy or mood. This is a direct miniature of the "rabbit-hole" problem that real platforms struggle with at billions-of-songs scale.

It also changed how I think about Spotify's "Discover Weekly." That feature feels magical, but underneath it is a much more complex version of the same idea: compare attributes, score, rank. The magic comes from having millions of users whose collective behaviour calibrates the weights automatically — something no hand-tuned system can replicate.

Human judgment still matters at every stage: deciding which features to include, how much weight each one deserves, what counts as a "correct" recommendation, and — most importantly — recognising when the system is reinforcing bias rather than serving the user.
