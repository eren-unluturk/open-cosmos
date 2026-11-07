# Safety spot-check (human review)

Labels were assigned by Claude Code (rules + hand-labeling) and have **not** been reviewed by a person. Please fill the **My verdict** column with `ok`, `too loose` (should be stricter) or `too strict` (should be looser). For `too loose`/`too strict`, you can also write the safety tier you want (`kid-safe`, `ask-a-grown-up`, `adult-only`) after the verdict, e.g. `too loose -> ask-a-grown-up`.

We classify titles, descriptions, categories and link hosts only, never the linked pages. Open the link if a row looks doubtful. Random picks use a fixed seed (2026), so this list is reproducible.

**Result (Eren, Nov 7):** all rows reviewed, every verdict `ok`; no overrides needed.

## A. 30 random kid-safe entries

| id | title | category | link host | topic | level | age_group | safety | safety_reasons | My verdict |
|---|---|---|---|---|---|---|---|---|---|
| learn-870c785a | Esolangs | Programming Languages | github.com | general | Intermediate | 11-13 | kid-safe | - |  |
| learn-36b92aaf | React Hooks | Front-End Development | github.com | web | Intermediate | teen+ | kid-safe | - |  |
| learn-4a78daa9 | F# | Programming Languages | github.com | general | Intermediate | teen+ | kid-safe | - |  |
| learn-16d19b2f | JavaScript | Programming Languages | github.com | web | Intermediate | teen+ | kid-safe | - |  |
| learn-7ed08f49 | Common Lisp | Programming Languages | github.com | general | Advanced | teen+ | kid-safe | - |  |
| kids-c04ee384 | Parity magic | CS Unplugged: Error detection  | csunplugged.org | general | Beginner | 8-10 | kid-safe | - |  |
| learn-815f486f | Colorful | Miscellaneous | github.com | art | Intermediate | 11-13 | kid-safe | - |  |
| learn-8147746d | Browser Extensions | Development Environment | github.com | web | Intermediate | teen+ | kid-safe | - |  |
| learn-171b13b5 | TensorFlow Lite | Computer Science | github.com | general | Advanced | teen+ | kid-safe | - |  |
| learn-c2d06255 | WebAssembly | Front-End Development | github.com | web | Advanced | teen+ | kid-safe | - |  |
| learn-cd095406 | Visual Regression Testing | Testing | github.com | web | Intermediate | teen+ | kid-safe | - |  |
| learn-c1486e86 | QR Code | Miscellaneous | github.com | general | Intermediate | teen+ | kid-safe | - |  |
| build-aeccd2f8 | How OpenGL works: software rendering in 500 lines of code | Build your own 3D Renderer | github.com | art | Advanced | teen+ | kid-safe | - |  |
| learn-dbebd220 | Core ML Models | Computer Science | github.com | general | Advanced | teen+ | kid-safe | - |  |
| learn-3f6c9d7d | Typing | Programming Languages | github.com | general | Intermediate | teen+ | kid-safe | - |  |
| kids-3135230d | Divide and conquer | CS Unplugged: Searching algori | csunplugged.org | general | Beginner | 5-7 | kid-safe | - |  |
| build-0e0ee2d4 | BYTEPATH | Build your own Game | github.com | games | Intermediate | teen+ | kid-safe | - |  |
| build-f3e0da40 | Write your own MVC from scratch in PHP | Uncategorized | chaitya62.github.io | web | Intermediate | teen+ | kid-safe | - |  |
| build-ab775371 | JavaScript Algorithms and Data Structures | Uncategorized | github.com | general | Intermediate | teen+ | kid-safe | - |  |
| learn-1b9d3696 | D | Programming Languages | github.com | general | Intermediate | teen+ | kid-safe | - |  |
| build-6d17c1f0 | Lexical Scanning in Go | Build your own Programming Lan | youtube.com | general | Intermediate | teen+ | kid-safe | - |  |
| build-fdb2cd89 | Learn how to write a hash table in C | Uncategorized | github.com | general | Intermediate | teen+ | kid-safe | - |  |
| learn-666aa764 | Natural Language Generation | Computer Science | github.com | general | Advanced | teen+ | kid-safe | - |  |
| learn-795c0520 | Vorpal | Miscellaneous | github.com | web | Intermediate | teen+ | kid-safe | - |  |
| learn-228a79e5 | Blazor | Front-End Development | github.com | web | Intermediate | teen+ | kid-safe | - |  |
| learn-f6a118f7 | Games of Coding | Gaming | github.com | general | Beginner | 8-10 | kid-safe | - |  |
| learn-e1f70867 | Scalability | Front-End Development | github.com | web | Advanced | teen+ | kid-safe | - |  |
| learn-8aaf5f49 | Chess | Gaming | github.com | games | Intermediate | 11-13 | kid-safe | - |  |
| learn-b2a338f8 | Katas | Miscellaneous | github.com | general | Intermediate | 11-13 | kid-safe | - |  |
| learn-f2aa26ad | Material Design | Front-End Development | github.com | web | Intermediate | teen+ | kid-safe | - |  |

## B. 15 random ask-a-grown-up entries (checking for ones that are too strict)

| id | title | category | link host | topic | level | age_group | safety | safety_reasons | My verdict |
|---|---|---|---|---|---|---|---|---|---|
| learn-78bb5e1f | Certificates | Learn | github.com | general | Intermediate | teen+ | ask-a-grown-up | account-required |  |
| build-878ecb32 | How to write a template engine in less than 30 lines of code | Build your own Template Engine | bits.citrusbyte.com | general | Intermediate | teen+ | ask-a-grown-up | unvetted-external-site |  |
| learn-1525081f | Gems | Back-End Development | github.com | other | Intermediate | teen+ | ask-a-grown-up | not-kid-oriented-topic |  |
| build-a986499c | Writing a Redis Protocol Parser | Uncategorized | xmonader.github.io | systems | Intermediate | teen+ | ask-a-grown-up | not-kid-oriented-topic, networking-tools |  |
| build-badbed13 | Tetris tutorial in C++ platform independent focused in game logic for  | Build your own Game | javilop.com | games | Beginner | 11-13 | ask-a-grown-up | unvetted-external-site |  |
| learn-7fe4f464 | Cybersecurity Blue Team | Security | github.com | security | Intermediate | teen+ | ask-a-grown-up | security-topic, not-kid-oriented-topic |  |
| build-d1d7cf94 | Let’s Write Redux! | Build your own Front-end Frame | jamasoftware.com | web | Intermediate | teen+ | ask-a-grown-up | unvetted-external-site |  |
| learn-04127162 | TinkerPop | Databases | github.com | systems | Advanced | teen+ | ask-a-grown-up | not-kid-oriented-topic |  |
| build-7be2eb80 | A cryptocurrency implementation in less than 1500 lines of code | Build your own Blockchain / Cr | github.com | systems | Intermediate | teen+ | ask-a-grown-up | finance-crypto, not-kid-oriented-topic |  |
| build-b8a6e4a5 | Learn & Build a JavaScript Blockchain | Build your own Blockchain / Cr | medium.com | systems | Intermediate | teen+ | ask-a-grown-up | finance-crypto, not-kid-oriented-topic, unvetted-external-site |  |
| build-122af213 | Build Your Own CLI App in Zig from Scratch | Build your own Command-Line To | rebuild-x.github.io | systems | Intermediate | teen+ | ask-a-grown-up | not-kid-oriented-topic |  |
| build-04a6ccc2 | Home-grown bytecode interpreters | Build your own Emulator / Virt | medium.com | systems | Advanced | teen+ | ask-a-grown-up | not-kid-oriented-topic, unvetted-external-site |  |
| learn-0e21e707 | Events in Italy | Events | github.com | other | Intermediate | teen+ | ask-a-grown-up | not-kid-oriented-topic, off-topic |  |
| build-8a6c038b | Computer Graphics from scratch | Build your own 3D Renderer | gabrielgambetta.com | art | Intermediate | teen+ | ask-a-grown-up | unvetted-external-site |  |
| learn-8971f417 | Digital History | Health and Social Science | github.com | other | Intermediate | teen+ | ask-a-grown-up | not-kid-oriented-topic |  |

## C. All 15 adult-only entries

| id | title | category | link host | topic | level | age_group | safety | safety_reasons | My verdict |
|---|---|---|---|---|---|---|---|---|---|
| build-6a273e43 | Hack the virtual memory | Build your own Operating Syste | blog.holbertonschool.com | security | Advanced | teen+ | adult-only | security-tooling, not-kid-oriented-topic, unvetted-external-site |  |
| learn-19b37b43 | CTF | Security | github.com | security | Intermediate | teen+ | adult-only | security-topic, not-kid-oriented-topic, security-tooling |  |
| learn-20cd67e3 | Lockpicking | Security | github.com | security | Intermediate | teen+ | adult-only | security-topic, not-kid-oriented-topic, security-tooling |  |
| learn-285fabbc | Suricata | Security | github.com | security | Advanced | teen+ | adult-only | security-topic, networking-tools, not-kid-oriented-topic, security-tooling |  |
| learn-288b2030 | Malware Persistence | Security | github.com | security | Advanced | teen+ | adult-only | security-tooling, security-topic, not-kid-oriented-topic |  |
| learn-4c37e33f | Honeypots | Security | github.com | security | Advanced | teen+ | adult-only | security-topic, not-kid-oriented-topic, security-tooling |  |
| learn-72abbe5f | Executable Packing | Security | github.com | security | Advanced | teen+ | adult-only | security-topic, not-kid-oriented-topic, security-tooling |  |
| learn-7cccf41a | Fuzzing | Security | github.com | security | Advanced | teen+ | adult-only | security-topic, not-kid-oriented-topic, security-tooling |  |
| learn-a832dd30 | Hacking Spots | Security | github.com | security | Intermediate | teen+ | adult-only | security-tooling, security-topic, not-kid-oriented-topic, unclear-content |  |
| learn-c087ea33 | Malware Analysis | Security | github.com | security | Intermediate | teen+ | adult-only | security-tooling, security-topic, not-kid-oriented-topic |  |
| learn-c2d10090 | Hacking | Security | github.com | security | Intermediate | teen+ | adult-only | security-tooling, security-topic, not-kid-oriented-topic |  |
| learn-cf5528aa | Tools of the Trade | Business | github.com | security | Intermediate | teen+ | adult-only | security-tooling, not-kid-oriented-topic, external-forum |  |
| learn-e9978cf5 | Password Cracking | Security | github.com | security | Intermediate | teen+ | adult-only | security-topic, not-kid-oriented-topic, security-tooling |  |
| learn-f5dec6ba | CI/CD Attacks | Security | github.com | security | Advanced | teen+ | adult-only | security-topic, not-kid-oriented-topic, security-tooling |  |
| learn-f99c2e98 | Vehicle Security and Car Hacking | Security | github.com | security | Intermediate | teen+ | adult-only | security-tooling, security-topic, not-kid-oriented-topic |  |

## D. 10 kid-safe entries with the youngest age_group and the rarest topic (CC0 sources only)


| id | title | category | link host | topic | level | age_group | safety | safety_reasons | My verdict |
|---|---|---|---|---|---|---|---|---|---|
| learn-6ed9a1c2 | ComputerCraft | Gaming | github.com | games | Beginner | 8-10 | kid-safe | - |  |
| learn-91178fe2 | Raspberry Pi | Platforms | github.com | general | Beginner | 8-10 | kid-safe | - |  |
| learn-c48f42e2 | Programming for Kids | Learn | github.com | general | Beginner | 8-10 | kid-safe | - |  |
| learn-ee67b89d | Educational Games | Learn | github.com | general | Beginner | 8-10 | kid-safe | - |  |
| learn-f6a118f7 | Games of Coding | Gaming | github.com | general | Beginner | 8-10 | kid-safe | - |  |
| build-25037537 | Introduction to Ray Tracing: a Simple Method for Creating 3D Images | Build your own 3D Renderer | scratchapixel.com | art | Beginner | 11-13 | kid-safe | - |  |
| learn-0bd65248 | Pixel Art | Media | github.com | art | Intermediate | 11-13 | kid-safe | - |  |
| learn-815f486f | Colorful | Miscellaneous | github.com | art | Intermediate | 11-13 | kid-safe | - |  |
| learn-96619f6f | Data Visualization | Miscellaneous | github.com | art | Intermediate | 11-13 | kid-safe | - |  |
| learn-a30fd642 | Design Principles | Miscellaneous | github.com | art | Intermediate | 11-13 | kid-safe | - |  |
