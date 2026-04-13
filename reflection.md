# Reflection: Music Recommender Simulation

## What was your biggest learning moment?

The biggest learning moment was realizing how much a recommender's behavior is shaped by **weights**, not the algorithm itself. When genre is worth 2.0 points and mood is worth 1.5, the system has a very different "personality" than if those numbers were swapped. There is no obviously correct answer — the weights are a judgment call, and without user feedback data to tune them, it is essentially a guess.

## How did using AI tools help you, and when did you need to double-check them?

AI tools helped me quickly brainstorm scoring strategies and understand the difference between collaborative filtering and content-based filtering. They were most useful for generating diverse song data for the CSV and suggesting the energy-proximity formula (1 − |song.energy − target|), which rewards closeness rather than just "higher is better." I needed to double-check suggestions around weight values — the AI would sometimes propose weights without justifying them, so I tested them manually with different profiles to see if the results made sense.

## What surprised you about how simple algorithms can still "feel" like recommendations?

I was surprised by how convincing the output looked for well-defined profiles. The Chill Lofi Listener got Midnight Coding and Library Rain as its top two results with scores above 5.0 — and those genuinely are the right answers. It felt intelligent, even though the logic underneath is just addition. The adversarial profile (ambient genre but high energy) broke the illusion quickly: genre won, and the top result was a soft ambient track despite the user wanting something high-energy. That gap between "feels smart" and "is smart" is exactly where real recommender systems invest enormous effort.

## Profile-by-Profile Comparison

**High-Energy Pop Fan vs. Chill Lofi Listener**
These two profiles produced completely non-overlapping top-5 lists. The pop fan got upbeat tracks (Sunrise City, Gym Hero); the lofi listener got quiet, acoustic tracks (Midnight Coding, Library Rain). This makes sense — genre and mood both flipped, so the scores diverged sharply. It validates that the system can distinguish between fundamentally different listening contexts.

**Chill Lofi Listener vs. Intense Rock Head**
Both profiles found a clear #1 (Midnight Coding and Storm Runner respectively), but the Rock Head's lower-ranked results were weaker — only one rock song exists in the catalog, so slots 2–5 filled with metal and high-energy non-rock tracks. This shows the system is limited by catalog diversity, not just logic.

**Intense Rock Head vs. Adversarial (conflicting prefs)**
The rock profile had a coherent top 5. The adversarial profile (ambient genre + high energy) showed the genre bonus dominating: Spacewalk Thoughts ranked first despite being low-energy and chill — the opposite of what the energy preference requested. This is the clearest evidence of genre dominance bias in the current scoring weights.

## What would you try next?

- Replace exact mood string matching with a similarity table so "focused" and "chill" earn partial credit instead of zero.
- Add a diversity penalty so the top 5 never includes more than two songs from the same genre.
- Expand the catalog to at least 100 songs so that niche genre matches have more than one result.
