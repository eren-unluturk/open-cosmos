# Translation queue (kid-safe entries not yet translated into es/ar/hi/pt)

Generated from `src/data/*.json` on Nov 7 2026. **401 entries** still need es, ar, hi and pt for `title` and `desc`. Priority order: CS Unplugged first, then Beginner, then Intermediate, then Advanced.

## Counts

| Source | Beginner | Intermediate | Advanced | Total |
|---|---|---|---|---|
| CS Unplugged | 24 | 0 | 0 | 24 |
| awesome | 0 | 258 | 65 | 323 |
| build-your-own-x | 0 | 36 | 18 | 54 |
| **All** | 24 | 294 | 83 | 401 |

## How to work through it
- Rules: keep code, product names and technical terms in English; translate prose only; put the languages you wrote into `ai_translated` on the entry; never change `level`, `age_group`, `safety` or `url`. CS Unplugged translations are CC BY-SA 4.0 adaptations (see `docs/SOURCES.md`).
- Split the list by block: e.g. rows 1-24 (CS Unplugged) first, then the Beginner rows, then Intermediate. Agree who takes which rows with Eren so edits don't collide in the JSON files.
- `python scripts/translate.py --limit N` does it with the API (needs a key; nobody has one right now). Careful: `--limit` is per file, and the script picks ANY entry missing a language, including `ask-a-grown-up` ones, in file order (kid-safe first, then Beginner first). It will reach the kid-safe ones first, but stop it after the kid-safe block unless you want everything. After each batch run `python -m unittest discover -s tests`.
- Still needs native-speaker checks for all four languages.

## Queue

| # | id | source | level | age | topic | title (en) |
|---|---|---|---|---|---|---|
| 1 | kids-38975fea | CS Unplugged | Beginner | 5-7 | general | Moving in a shape |
| 2 | kids-4245fca0 | CS Unplugged | Beginner | 5-7 | general | Finding shapes |
| 3 | kids-74ac9c1a | CS Unplugged | Beginner | 5-7 | general | Growing into a butterfly |
| 4 | kids-caecb6de | CS Unplugged | Beginner | 5-7 | general | Move to a number |
| 5 | kids-d76340f4 | CS Unplugged | Beginner | 5-7 | general | Retelling a story |
| 6 | kids-db747678 | CS Unplugged | Beginner | 5-7 | general | Storytelling |
| 7 | kids-0e0fd64c | CS Unplugged | Beginner | 8-10 | art | Binary Art |
| 8 | kids-15f1c61e | CS Unplugged | Beginner | 8-10 | general | What if? |
| 9 | kids-1e418bb2 | CS Unplugged | Beginner | 8-10 | general | Whose cake is it |
| 10 | kids-1f9fce96 | CS Unplugged | Beginner | 8-10 | general | Binary Candles or Normal Candles on your Cake |
| 11 | kids-1fa4226b | CS Unplugged | Beginner | 8-10 | general | How binary digits work: programming challenges |
| 12 | kids-4a52187c | CS Unplugged | Beginner | 8-10 | art | Music activity |
| 13 | kids-5cc52bdb | CS Unplugged | Beginner | 8-10 | art | Binary Tunes |
| 14 | kids-628ca386 | CS Unplugged | Beginner | 8-10 | general | Drama or video activity |
| 15 | kids-62b8fce9 | CS Unplugged | Beginner | 8-10 | general | Word study activity |
| 16 | kids-882ed275 | CS Unplugged | Beginner | 8-10 | general | Instructional writing |
| 17 | kids-888168fc | CS Unplugged | Beginner | 8-10 | general | Sending a rocket to Mars: programming challenges |
| 18 | kids-a25e1b00 | CS Unplugged | Beginner | 8-10 | general | Parity magic: programming challenges |
| 19 | kids-d72c2c6b | CS Unplugged | Beginner | 8-10 | general | The Modulo operator Unplugged: programming challenges |
| 20 | kids-d9fc78be | CS Unplugged | Beginner | 8-10 | art | Binary Patterns |
| 21 | kids-dec7dc4e | CS Unplugged | Beginner | 8-10 | general | Product code check digits: programming challenges |
| 22 | kids-e7a2b929 | CS Unplugged | Beginner | 8-10 | general | Quick card flip magic |
| 23 | kids-ebc5a5ff | CS Unplugged | Beginner | 8-10 | general | Where is my hat? |
| 24 | kids-f336b2e4 | CS Unplugged | Beginner | 8-10 | art | Binary Name Necklaces |
| 25 | build-16587794 | build-your-own-x | Intermediate | 11-13 | games | Build your own 8-Ball Pool game from scratch |
| 26 | learn-041e4cc2 | awesome | Intermediate | 11-13 | games | Godot |
| 27 | learn-0a0d36e1 | awesome | Intermediate | 11-13 | games | Game Development |
| 28 | learn-0bd65248 | awesome | Intermediate | 11-13 | art | Pixel Art |
| 29 | learn-11bef6ff | awesome | Intermediate | 11-13 | games | GameMaker |
| 30 | learn-13e0a239 | awesome | Intermediate | 11-13 | general | Awesome |
| 31 | learn-201f2b16 | awesome | Intermediate | 11-13 | general | Python |
| 32 | learn-2c2fe965 | awesome | Intermediate | 11-13 | general | Education |
| 33 | learn-3f9c6545 | awesome | Intermediate | 11-13 | web | Web Accessibility |
| 34 | learn-560b0354 | awesome | Intermediate | 11-13 | general | Learning |
| 35 | learn-5c36a179 | awesome | Intermediate | 11-13 | games | Open Source Games |
| 36 | learn-63a967ca | awesome | Intermediate | 11-13 | general | Creative Coding |
| 37 | learn-6860996c | awesome | Intermediate | 11-13 | games | Flame |
| 38 | learn-69b930f2 | awesome | Intermediate | 11-13 | web | Web Animation |
| 39 | learn-6fda3a6c | awesome | Intermediate | 11-13 | general | Lua |
| 40 | learn-70e1be9a | awesome | Intermediate | 11-13 | web | Flexbox |
| 41 | learn-756e951b | awesome | Intermediate | 11-13 | web | Canvas |
| 42 | learn-815f486f | awesome | Intermediate | 11-13 | art | Colorful |
| 43 | learn-870c785a | awesome | Intermediate | 11-13 | general | Esolangs |
| 44 | learn-8aaf5f49 | awesome | Intermediate | 11-13 | games | Chess |
| 45 | learn-8cc4faa3 | awesome | Intermediate | 11-13 | web | CSS |
| 46 | learn-909c3360 | awesome | Intermediate | 11-13 | general | Education |
| 47 | learn-912c59a5 | awesome | Intermediate | 11-13 | games | Gideros |
| 48 | learn-96619f6f | awesome | Intermediate | 11-13 | art | Data Visualization |
| 49 | learn-a30fd642 | awesome | Intermediate | 11-13 | art | Design Principles |
| 50 | learn-a5a667f5 | awesome | Intermediate | 11-13 | general | Playgrounds |
| 51 | learn-a838865a | awesome | Intermediate | 11-13 | general | Algorithm Visualizations |
| 52 | learn-aa33d325 | awesome | Intermediate | 11-13 | general | Free Programming Books |
| 53 | learn-b2a338f8 | awesome | Intermediate | 11-13 | general | Katas |
| 54 | learn-b373d1c2 | awesome | Intermediate | 11-13 | art | Screensavers |
| 55 | learn-b9e65004 | awesome | Intermediate | 11-13 | general | Algorithms |
| 56 | learn-c05b83f3 | awesome | Intermediate | 11-13 | general | Spanish |
| 57 | learn-c563507a | awesome | Intermediate | 11-13 | general | Learning |
| 58 | learn-cab71370 | awesome | Intermediate | 11-13 | web | SVG |
| 59 | learn-d828206b | awesome | Intermediate | 11-13 | art | Icons |
| 60 | learn-e27a486c | awesome | Intermediate | 11-13 | web | HTML5 |
| 61 | learn-e8c9a498 | awesome | Intermediate | 11-13 | games | Construct 2 |
| 62 | learn-f2a21163 | awesome | Intermediate | 11-13 | web | Web Design |
| 63 | learn-f716942b | awesome | Intermediate | 11-13 | general | Education |
| 64 | learn-fc7650fc | awesome | Intermediate | 11-13 | general | Math |
| 65 | build-021ddad9 | build-your-own-x | Intermediate | teen+ | general | Writing a Link Checker |
| 66 | build-05969466 | build-your-own-x | Intermediate | teen+ | web | lets-build-express |
| 67 | build-15e24f81 | build-your-own-x | Intermediate | teen+ | games | How To Unity ARCore |
| 68 | build-1eefac4d | build-your-own-x | Intermediate | teen+ | general | A Neural Network in 11 lines of Python |
| 69 | build-25d276a6 | build-your-own-x | Intermediate | teen+ | games | Coding a Rogue/Nethack RPG in C |
| 70 | build-2785ade2 | build-your-own-x | Intermediate | teen+ | general | How to Augmented Reality AR Tutorial: ARKit Portal to the Upside Down |
| 71 | build-27f27e0a | build-your-own-x | Intermediate | teen+ | games | Roguelike Tutorial in Rust + tcod |
| 72 | build-28a71ea2 | build-your-own-x | Intermediate | teen+ | general | Continuous Integration System |
| 73 | build-361c58ea | build-your-own-x | Intermediate | teen+ | general | Writing a MiniTest Framework |
| 74 | build-4c870d39 | build-your-own-x | Intermediate | teen+ | art | Build your own 3D renderer |
| 75 | build-55f98526 | build-your-own-x | Intermediate | teen+ | web | Writing a URL Shortening Service |
| 76 | build-62aac5fc | build-your-own-x | Intermediate | teen+ | general | A Template Engine |
| 77 | build-6716814f | build-your-own-x | Intermediate | teen+ | games | Coding A Sudoku Solver in C |
| 78 | build-67cc0442 | build-your-own-x | Intermediate | teen+ | general | Neural Networks: Zero to Hero |
| 79 | build-6a17accb | build-your-own-x | Intermediate | teen+ | web | Building a frontend framework, from scratch, with components (templati |
| 80 | build-6d17c1f0 | build-your-own-x | Intermediate | teen+ | general | Lexical Scanning in Go |
| 81 | build-75ee0c25 | build-your-own-x | Intermediate | teen+ | games | AR Portal Tutorial with Unity |
| 82 | build-760f10e2 | build-your-own-x | Intermediate | teen+ | general | Tiny Package Manager: Learns how npm or Yarn works |
| 83 | build-7ae22b77 | build-your-own-x | Intermediate | teen+ | games | How to create a Dragon in Augmented Reality in Unity ARCore |
| 84 | build-961a5b5f | build-your-own-x | Intermediate | teen+ | games | Let's Make: Dangerous Dave |
| 85 | build-a11ba8c6 | build-your-own-x | Intermediate | teen+ | web | Build Your Own Module Bundler - Minipack |
| 86 | build-a6c99700 | build-your-own-x | Intermediate | teen+ | general | Building A Python-Based Search Engine |
| 87 | build-ab775371 | build-your-own-x | Intermediate | teen+ | general | JavaScript Algorithms and Data Structures |
| 88 | build-c0c5d580 | build-your-own-x | Intermediate | teen+ | general | mal - Make a Lisp |
| 89 | build-c238feec | build-your-own-x | Intermediate | teen+ | art | A 3D Modeller |
| 90 | build-c28cc666 | build-your-own-x | Intermediate | teen+ | general | JSON Decoding Algorithm |
| 91 | build-ccdcf9db | build-your-own-x | Intermediate | teen+ | web | How to create a real-world Node CLI app with Node |
| 92 | build-d12c8bbc | build-your-own-x | Intermediate | teen+ | games | Games With Go |
| 93 | build-d51d79db | build-your-own-x | Intermediate | teen+ | web | Neural Networks - The Nature of Code |
| 94 | build-d8acae03 | build-your-own-x | Intermediate | teen+ | general | Python Tutorial: Make Your Own Text Editor |
| 95 | build-e8ae0363 | build-your-own-x | Intermediate | teen+ | games | Learn Video Game Programming in C |
| 96 | build-f3e0da40 | build-your-own-x | Intermediate | teen+ | web | Write your own MVC from scratch in PHP |
| 97 | build-f9f9837c | build-your-own-x | Intermediate | teen+ | art | Rasterization: a Practical Implementation |
| 98 | build-fdaf1687 | build-your-own-x | Intermediate | teen+ | web | A DIY guide to build your own React |
| 99 | build-fdb2cd89 | build-your-own-x | Intermediate | teen+ | general | Learn how to write a hash table in C |
| 100 | learn-010606a9 | awesome | Intermediate | teen+ | general | Testing |
| 101 | learn-02282bb3 | awesome | Intermediate | teen+ | web | Sass |
| 102 | learn-02647a3f | awesome | Intermediate | teen+ | general | Speaking |
| 103 | learn-059b8c49 | awesome | Intermediate | teen+ | general | JSON |
| 104 | learn-059eabcc | awesome | Intermediate | teen+ | web | Tiny JS |
| 105 | learn-05d31f6f | awesome | Intermediate | teen+ | web | Inspiration |
| 106 | learn-061273e2 | awesome | Intermediate | teen+ | general | Elixir Books |
| 107 | learn-0699cf70 | awesome | Intermediate | teen+ | web | ES6 Tools |
| 108 | learn-06b6370e | awesome | Intermediate | teen+ | web | WebExtensions |
| 109 | learn-07de4fa6 | awesome | Intermediate | teen+ | art | Audio Visualization |
| 110 | learn-0a8d26e8 | awesome | Intermediate | teen+ | general | Java |
| 111 | learn-0b9fc4cb | awesome | Intermediate | teen+ | art | Product Design |
| 112 | learn-0bfcf3f0 | awesome | Intermediate | teen+ | general | Data Science |
| 113 | learn-0d4bd10a | awesome | Intermediate | teen+ | web | Svelte |
| 114 | learn-0e4f10f0 | awesome | Intermediate | teen+ | web | lit |
| 115 | learn-0e81811d | awesome | Intermediate | teen+ | web | PageSpeed Metrics |
| 116 | learn-0ed171df | awesome | Intermediate | teen+ | web | Search Engine Optimization |
| 117 | learn-0fcd0421 | awesome | Intermediate | teen+ | general | Regex |
| 118 | learn-136ee9a2 | awesome | Intermediate | teen+ | web | Backbone |
| 119 | learn-15c5debf | awesome | Intermediate | teen+ | web | WebXR |
| 120 | learn-15f5ae21 | awesome | Intermediate | teen+ | general | Tech Videos |
| 121 | learn-16d19b2f | awesome | Intermediate | teen+ | web | JavaScript |
| 122 | learn-16e4820d | awesome | Intermediate | teen+ | web | Sitecore |
| 123 | learn-17c1e9b6 | awesome | Intermediate | teen+ | web | Static Website Services |
| 124 | learn-18e73173 | awesome | Intermediate | teen+ | general | Education |
| 125 | learn-1980376c | awesome | Intermediate | teen+ | general | NLP with Ruby |
| 126 | learn-1b9d3696 | awesome | Intermediate | teen+ | general | D |
| 127 | learn-1bada5df | awesome | Intermediate | teen+ | general | Naming |
| 128 | learn-1ce410e7 | awesome | Intermediate | teen+ | general | Product Management |
| 129 | learn-1d430314 | awesome | Intermediate | teen+ | general | Software Engineering Blogs |
| 130 | learn-1e3f3205 | awesome | Intermediate | teen+ | web | Web Archiving |
| 131 | learn-2026e8a8 | awesome | Intermediate | teen+ | general | Must Watch Talks |
| 132 | learn-210cc042 | awesome | Intermediate | teen+ | web | Must-Watch Talks |
| 133 | learn-228a79e5 | awesome | Intermediate | teen+ | web | Blazor |
| 134 | learn-2408990a | awesome | Intermediate | teen+ | web | Electron |
| 135 | learn-26da6b4a | awesome | Intermediate | teen+ | general | npm scripts |
| 136 | learn-27e0a052 | awesome | Intermediate | teen+ | web | PostCSS |
| 137 | learn-27ed50cc | awesome | Intermediate | teen+ | general | Elixir |
| 138 | learn-28b0f1df | awesome | Intermediate | teen+ | general | Talks |
| 139 | learn-290ae11a | awesome | Intermediate | teen+ | web | Drupal |
| 140 | learn-2aa562be | awesome | Intermediate | teen+ | web | Frameworks |
| 141 | learn-2ac59774 | awesome | Intermediate | teen+ | web | REST |
| 142 | learn-2d24b9c3 | awesome | Intermediate | teen+ | art | Open Source Photography |
| 143 | learn-2df92a72 | awesome | Intermediate | teen+ | web | Phalcon |
| 144 | learn-2e129b6d | awesome | Intermediate | teen+ | games | Game Remakes |
| 145 | learn-30949ba7 | awesome | Intermediate | teen+ | general | Dart |
| 146 | learn-312db5d1 | awesome | Intermediate | teen+ | web | Charting |
| 147 | learn-3172c479 | awesome | Intermediate | teen+ | art | Creative Technology |
| 148 | learn-319d0668 | awesome | Intermediate | teen+ | general | Plone |
| 149 | learn-32521322 | awesome | Intermediate | teen+ | general | CSV |
| 150 | learn-3281aaed | awesome | Intermediate | teen+ | general | AutoHotkey |
| 151 | learn-329f7c09 | awesome | Intermediate | teen+ | general | Unicode |
| 152 | learn-337572ad | awesome | Intermediate | teen+ | web | MDBootstrap |
| 153 | learn-35195ff0 | awesome | Intermediate | teen+ | general | Static Analysis & Code Quality |
| 154 | learn-362cd209 | awesome | Intermediate | teen+ | web | Web Performance Optimization |
| 155 | learn-36b92aaf | awesome | Intermediate | teen+ | web | React Hooks |
| 156 | learn-3947ef91 | awesome | Intermediate | teen+ | general | R Books |
| 157 | learn-3a9e5234 | awesome | Intermediate | teen+ | web | Node.js |
| 158 | learn-3b12be6a | awesome | Intermediate | teen+ | web | Less |
| 159 | learn-3bafd5fb | awesome | Intermediate | teen+ | art | TikZ |
| 160 | learn-3bf77272 | awesome | Intermediate | teen+ | web | Dojo Toolkit |
| 161 | learn-3e11113c | awesome | Intermediate | teen+ | web | CakePHP |
| 162 | learn-3f6c9d7d | awesome | Intermediate | teen+ | general | Typing |
| 163 | learn-3f9ff83f | awesome | Intermediate | teen+ | general | Maintenance Modules |
| 164 | learn-410647e2 | awesome | Intermediate | teen+ | general | Elm |
| 165 | learn-4160a0f0 | awesome | Intermediate | teen+ | general | Kotlin |
| 166 | learn-4380890d | awesome | Intermediate | teen+ | web | Web Audio |
| 167 | learn-4552bded | awesome | Intermediate | teen+ | web | Vue.js |
| 168 | learn-45f3f83e | awesome | Intermediate | teen+ | general | Mad Science npm Packages |
| 169 | learn-4710560f | awesome | Intermediate | teen+ | general | Read the Docs |
| 170 | learn-474c52c7 | awesome | Intermediate | teen+ | general | J2ME |
| 171 | learn-4897ef29 | awesome | Intermediate | teen+ | general | Falsehood |
| 172 | learn-4a70f925 | awesome | Intermediate | teen+ | web | nginx |
| 173 | learn-4a78daa9 | awesome | Intermediate | teen+ | general | F# |
| 174 | learn-4ad1f621 | awesome | Intermediate | teen+ | web | Meteor |
| 175 | learn-4b1f8fcb | awesome | Intermediate | teen+ | art | Generative AI |
| 176 | learn-4bc3fbbe | awesome | Intermediate | teen+ | web | SAP Commerce |
| 177 | learn-4d89aca2 | awesome | Intermediate | teen+ | general | Code Points |
| 178 | learn-4e330ff3 | awesome | Intermediate | teen+ | art | Plotters |
| 179 | learn-4eadffdb | awesome | Intermediate | teen+ | web | FastAPI |
| 180 | learn-4f54d0f5 | awesome | Intermediate | teen+ | web | Fiber |
| 181 | learn-4f9e33c7 | awesome | Intermediate | teen+ | art | FFmpeg |
| 182 | learn-50397e3e | awesome | Intermediate | teen+ | art | Fonts |
| 183 | learn-50825303 | awesome | Intermediate | teen+ | general | Functional Programming |
| 184 | learn-50a51bf4 | awesome | Intermediate | teen+ | general | Mind Expanding Books |
| 185 | learn-512c2773 | awesome | Intermediate | teen+ | games | Game Boy Development |
| 186 | learn-51aa9181 | awesome | Intermediate | teen+ | general | CMake |
| 187 | learn-535ea0a4 | awesome | Intermediate | teen+ | web | iOS UI |
| 188 | learn-5382d6e0 | awesome | Intermediate | teen+ | general | Clojure |
| 189 | learn-55e210eb | awesome | Intermediate | teen+ | general | .NET |
| 190 | learn-5a4a20ed | awesome | Intermediate | teen+ | web | Deno |
| 191 | learn-5a988e3b | awesome | Intermediate | teen+ | web | Amazon Web Services |
| 192 | learn-5c9e6ecf | awesome | Intermediate | teen+ | general | ActionScript 3 |
| 193 | learn-5dd9f6ed | awesome | Intermediate | teen+ | web | Scriptable |
| 194 | learn-5e6c6370 | awesome | Intermediate | teen+ | art | Audiovisual |
| 195 | learn-5e7b747b | awesome | Intermediate | teen+ | web | Motion UI Design |
| 196 | learn-5ee234db | awesome | Intermediate | teen+ | web | Umbraco |
| 197 | learn-5f96924b | awesome | Intermediate | teen+ | web | Play1 Framework |
| 198 | learn-604e86a5 | awesome | Intermediate | teen+ | art | GIF |
| 199 | learn-65d62bbf | awesome | Intermediate | teen+ | web | Angular |
| 200 | learn-6690262b | awesome | Intermediate | teen+ | general | Low Code |
| 201 | learn-6764d0ed | awesome | Intermediate | teen+ | general | Promises |
| 202 | learn-68fd5d71 | awesome | Intermediate | teen+ | general | Composer |
| 203 | learn-6a6c2e20 | awesome | Intermediate | teen+ | web | Design and Development Guides |
| 204 | learn-6be895bc | awesome | Intermediate | teen+ | general | Hackathon |
| 205 | learn-6e132d82 | awesome | Intermediate | teen+ | web | Apache Wicket |
| 206 | learn-75da339d | awesome | Intermediate | teen+ | web | Slim |
| 207 | learn-76bea68c | awesome | Intermediate | teen+ | general | Competitive Programming |
| 208 | learn-76ebe071 | awesome | Intermediate | teen+ | web | Protips |
| 209 | learn-77e350a6 | awesome | Intermediate | teen+ | games | Babylon.js |
| 210 | learn-78dd1ce6 | awesome | Intermediate | teen+ | web | Wagtail |
| 211 | learn-795c0520 | awesome | Intermediate | teen+ | web | Vorpal |
| 212 | learn-7960c641 | awesome | Intermediate | teen+ | web | Web Typography |
| 213 | learn-7bff144d | awesome | Intermediate | teen+ | web | Symfony |
| 214 | learn-7c1b2e0a | awesome | Intermediate | teen+ | web | WebGL |
| 215 | learn-7f044f2f | awesome | Intermediate | teen+ | web | Selenium |
| 216 | learn-8147746d | awesome | Intermediate | teen+ | web | Browser Extensions |
| 217 | learn-845d1d23 | awesome | Intermediate | teen+ | web | Frontend Development |
| 218 | learn-863391f5 | awesome | Intermediate | teen+ | general | Pascal |
| 219 | learn-8b2968ba | awesome | Intermediate | teen+ | general | Education |
| 220 | learn-9074c352 | awesome | Intermediate | teen+ | web | Text Editing |
| 221 | learn-908dae14 | awesome | Intermediate | teen+ | general | C/C++ |
| 222 | learn-90fb074f | awesome | Intermediate | teen+ | web | Framer |
| 223 | learn-936d4682 | awesome | Intermediate | teen+ | web | React Native |
| 224 | learn-9aa8ebe3 | awesome | Intermediate | teen+ | general | AutoIt |
| 225 | learn-9b7dd79d | awesome | Intermediate | teen+ | web | Dash |
| 226 | learn-9b9b9adc | awesome | Intermediate | teen+ | general | Data Science |
| 227 | learn-9c58a9f5 | awesome | Intermediate | teen+ | web | choo |
| 228 | learn-a0ea5af6 | awesome | Intermediate | teen+ | web | Lumen |
| 229 | learn-a18cd8d2 | awesome | Intermediate | teen+ | web | Ionic Framework |
| 230 | learn-a1de233d | awesome | Intermediate | teen+ | web | Dropwizard |
| 231 | learn-a21c0b8a | awesome | Intermediate | teen+ | general | R |
| 232 | learn-a2a01b5f | awesome | Intermediate | teen+ | web | Payload |
| 233 | learn-a2a85129 | awesome | Intermediate | teen+ | web | Aurelia |
| 234 | learn-a34d892e | awesome | Intermediate | teen+ | web | Gulp |
| 235 | learn-a41a2cbe | awesome | Intermediate | teen+ | general | Open Source Society University |
| 236 | learn-a4d22b04 | awesome | Intermediate | teen+ | web | Userscripts |
| 237 | learn-a742688f | awesome | Intermediate | teen+ | web | Biological Visualizations |
| 238 | learn-a8dc24fd | awesome | Intermediate | teen+ | art | VLC |
| 239 | learn-a9b68eb1 | awesome | Intermediate | teen+ | web | Android UI |
| 240 | learn-aa0200fd | awesome | Intermediate | teen+ | art | Music |
| 241 | learn-ab1cc51f | awesome | Intermediate | teen+ | web | Design systems |
| 242 | learn-ab2c219a | awesome | Intermediate | teen+ | web | Draft.js |
| 243 | learn-ab969ada | awesome | Intermediate | teen+ | web | Silverstripe CMS |
| 244 | learn-aba72944 | awesome | Intermediate | teen+ | general | Tips |
| 245 | learn-ac95d8c5 | awesome | Intermediate | teen+ | general | Rust |
| 246 | learn-aca21a9a | awesome | Intermediate | teen+ | general | Linguistics |
| 247 | learn-ad1072de | awesome | Intermediate | teen+ | web | D3 |
| 248 | learn-ad89662c | awesome | Intermediate | teen+ | web | Tips |
| 249 | learn-ae3f04e7 | awesome | Intermediate | teen+ | web | Web Tools |
| 250 | learn-b3c30fae | awesome | Intermediate | teen+ | general | Ruby |
| 251 | learn-b5af35c8 | awesome | Intermediate | teen+ | general | Node-RED |
| 252 | learn-b66eb4ad | awesome | Intermediate | teen+ | web | Cross-Platform |
| 253 | learn-b674d108 | awesome | Intermediate | teen+ | general | Swift |
| 254 | learn-b94bf5f9 | awesome | Intermediate | teen+ | web | Master CSS |
| 255 | learn-bb120595 | awesome | Intermediate | teen+ | general | Go Books |
| 256 | learn-bb91aa40 | awesome | Intermediate | teen+ | web | Useful .htaccess Snippets |
| 257 | learn-bccc5beb | awesome | Intermediate | teen+ | web | Emails |
| 258 | learn-bd1d4010 | awesome | Intermediate | teen+ | general | University Courses |
| 259 | learn-bdc65c6f | awesome | Intermediate | teen+ | general | Micro npm Packages |
| 260 | learn-be51c90e | awesome | Intermediate | teen+ | art | Stock Resources |
| 261 | learn-bfcea038 | awesome | Intermediate | teen+ | general | Pyramid |
| 262 | learn-c0b4c604 | awesome | Intermediate | teen+ | general | Flask |
| 263 | learn-c1486e86 | awesome | Intermediate | teen+ | general | QR Code |
| 264 | learn-c17ba638 | awesome | Intermediate | teen+ | web | Mobile Web Development |
| 265 | learn-c1897ebf | awesome | Intermediate | teen+ | web | Web Performance Budget |
| 266 | learn-c360eafa | awesome | Intermediate | teen+ | web | Progressive Enhancement |
| 267 | learn-c3f955b8 | awesome | Intermediate | teen+ | web | React |
| 268 | learn-c5f28ddc | awesome | Intermediate | teen+ | web | WordPress-Gatsby |
| 269 | learn-c6dd2618 | awesome | Intermediate | teen+ | web | Polymer |
| 270 | learn-c72fdd95 | awesome | Intermediate | teen+ | web | Reflex |
| 271 | learn-c83f83bc | awesome | Intermediate | teen+ | general | ESLint |
| 272 | learn-cb0a8e44 | awesome | Intermediate | teen+ | general | ML with Ruby |
| 273 | learn-cb6c86c5 | awesome | Intermediate | teen+ | web | Storybook |
| 274 | learn-cba9ba60 | awesome | Intermediate | teen+ | web | Next.js |
| 275 | learn-cbe7c340 | awesome | Intermediate | teen+ | web | Magento 2 |
| 276 | learn-cc8c264b | awesome | Intermediate | teen+ | web | Progressive Web Apps |
| 277 | learn-cd095406 | awesome | Intermediate | teen+ | web | Visual Regression Testing |
| 278 | learn-cef56a91 | awesome | Intermediate | teen+ | web | Cordova |
| 279 | learn-cf448cc4 | awesome | Intermediate | teen+ | general | Book Authoring |
| 280 | learn-d15ace71 | awesome | Intermediate | teen+ | games | CHIP-8 |
| 281 | learn-d1d1f7ff | awesome | Intermediate | teen+ | general | npm |
| 282 | learn-d38bd96e | awesome | Intermediate | teen+ | web | Refinery CMS |
| 283 | learn-d41abc21 | awesome | Intermediate | teen+ | web | Ant Design |
| 284 | learn-d5386503 | awesome | Intermediate | teen+ | web | Textpattern |
| 285 | learn-d5b17289 | awesome | Intermediate | teen+ | web | Material-UI |
| 286 | learn-d672c131 | awesome | Intermediate | teen+ | web | Building Blocks for Web Apps |
| 287 | learn-d90cfcbb | awesome | Intermediate | teen+ | web | BEM |
| 288 | learn-daa2446b | awesome | Intermediate | teen+ | games | Haxe Game Development |
| 289 | learn-db5fb6b7 | awesome | Intermediate | teen+ | web | Browserify |
| 290 | learn-dbba4056 | awesome | Intermediate | teen+ | web | Playwright |
| 291 | learn-dcb5cdf5 | awesome | Intermediate | teen+ | general | Codeface |
| 292 | learn-de8e9f56 | awesome | Intermediate | teen+ | web | GraphQL |
| 293 | learn-e13a52bc | awesome | Intermediate | teen+ | web | Critical-Path Tools |
| 294 | learn-e2d71c25 | awesome | Intermediate | teen+ | web | Capacitor |
| 295 | learn-e37b88c4 | awesome | Intermediate | teen+ | web | WP-CLI |
| 296 | learn-e3b96168 | awesome | Intermediate | teen+ | general | Go |
| 297 | learn-e44c8d6a | awesome | Intermediate | teen+ | general | Imba |
| 298 | learn-e855f3f3 | awesome | Intermediate | teen+ | general | ColdFusion |
| 299 | learn-e87f840f | awesome | Intermediate | teen+ | web | Marionette.js |
| 300 | learn-e980316d | awesome | Intermediate | teen+ | web | Inertia.js |
| 301 | learn-e9d4ee24 | awesome | Intermediate | teen+ | web | Ember |
| 302 | learn-ea7d5fde | awesome | Intermediate | teen+ | general | Perl |
| 303 | learn-eb35fbe3 | awesome | Intermediate | teen+ | web | Hyper |
| 304 | learn-eb89f448 | awesome | Intermediate | teen+ | web | Chrome DevTools |
| 305 | learn-ebcfca04 | awesome | Intermediate | teen+ | general | Standard Style |
| 306 | learn-ecc897b0 | awesome | Intermediate | teen+ | web | KnockoutJS |
| 307 | learn-eeb78cd4 | awesome | Intermediate | teen+ | web | Preact |
| 308 | learn-f0b42e1d | awesome | Intermediate | teen+ | games | Game Talks |
| 309 | learn-f2aa26ad | awesome | Intermediate | teen+ | web | Material Design |
| 310 | learn-f3119b47 | awesome | Intermediate | teen+ | general | PHP |
| 311 | learn-f4e78a20 | awesome | Intermediate | teen+ | general | Conversational AI |
| 312 | learn-f5c4ed27 | awesome | Intermediate | teen+ | general | AVA |
| 313 | learn-f715f6ec | awesome | Intermediate | teen+ | web | Laravel |
| 314 | learn-fa101958 | awesome | Intermediate | teen+ | games | libGDX |
| 315 | learn-fa128a35 | awesome | Intermediate | teen+ | web | Rails |
| 316 | learn-fbd2a0bc | awesome | Intermediate | teen+ | web | JAMstack |
| 317 | learn-fc038e95 | awesome | Intermediate | teen+ | web | Redux |
| 318 | learn-fc98a49c | awesome | Intermediate | teen+ | games | PlayCanvas |
| 319 | build-0154ebfa | build-your-own-x | Advanced | teen+ | general | SlowTorch: Implementation of PyTorch from the ground up in 100% pure P |
| 320 | build-0dd2a748 | build-your-own-x | Advanced | teen+ | games | Reconstructing Cave Story |
| 321 | build-1b76c92d | build-your-own-x | Advanced | teen+ | general | Build a Deep Learning Library |
| 322 | build-1f1bc03a | build-your-own-x | Advanced | teen+ | general | A Large Language Model (LLM) |
| 323 | build-2156aefb | build-your-own-x | Advanced | teen+ | web | Building React From Scratch |
| 324 | build-28348eb1 | build-your-own-x | Advanced | teen+ | art | 3D Physics Engine Tutorial |
| 325 | build-2cf54114 | build-your-own-x | Advanced | teen+ | general | Optical Character Recognition (OCR) |
| 326 | build-514158f4 | build-your-own-x | Advanced | teen+ | art | Ray Tracing in One Weekend |
| 327 | build-5ab37fe3 | build-your-own-x | Advanced | teen+ | games | Make your own Game Engine |
| 328 | build-69566814 | build-your-own-x | Advanced | teen+ | general | Build Deep Learning From Scratch (reimplement PyTorch internals across |
| 329 | build-9ab4653e | build-your-own-x | Advanced | teen+ | general | RAG for Document Search |
| 330 | build-aeccd2f8 | build-your-own-x | Advanced | teen+ | art | How OpenGL works: software rendering in 500 lines of code |
| 331 | build-bcb475f9 | build-your-own-x | Advanced | teen+ | general | Creating JVM Language |
| 332 | build-d68ab5c2 | build-your-own-x | Advanced | teen+ | web | Building a Custom React Renderer |
| 333 | build-dbc6b593 | build-your-own-x | Advanced | teen+ | games | Remaking Cavestory in C++ |
| 334 | build-ebb0d512 | build-your-own-x | Advanced | teen+ | games | Chess Engine In C |
| 335 | build-f459bc96 | build-your-own-x | Advanced | teen+ | general | A Python Interpreter Written in Python |
| 336 | build-fb216e8e | build-your-own-x | Advanced | teen+ | general | Jonesforth |
| 337 | learn-01b8fcea | awesome | Advanced | teen+ | general | Scala Native |
| 338 | learn-06989e0f | awesome | Advanced | teen+ | web | Relay |
| 339 | learn-0db64ee0 | awesome | Advanced | teen+ | web | Frontend GIS |
| 340 | learn-122117c4 | awesome | Advanced | teen+ | web | Web Components |
| 341 | learn-131a52a2 | awesome | Advanced | teen+ | general | Question Answering |
| 342 | learn-1418a550 | awesome | Advanced | teen+ | general | Recursion Schemes |
| 343 | learn-171b13b5 | awesome | Advanced | teen+ | general | TensorFlow Lite |
| 344 | learn-18a80f99 | awesome | Advanced | teen+ | general | JAX |
| 345 | learn-1c4e452f | awesome | Advanced | teen+ | general | Q# |
| 346 | learn-21c37b3f | awesome | Advanced | teen+ | general | Empirical Software Engineering |
| 347 | learn-26554baf | awesome | Advanced | teen+ | general | Quantum Computing |
| 348 | learn-33d21ae1 | awesome | Advanced | teen+ | general | Papers |
| 349 | learn-3765ef2a | awesome | Advanced | teen+ | games | Game Datasets |
| 350 | learn-48ecfbb7 | awesome | Advanced | teen+ | general | Scientific Audio |
| 351 | learn-49089992 | awesome | Advanced | teen+ | web | Service Workers |
| 352 | learn-4f68305c | awesome | Advanced | teen+ | general | Deep Learning |
| 353 | learn-4fb0f569 | awesome | Advanced | teen+ | general | Coq |
| 354 | learn-50b06fb3 | awesome | Advanced | teen+ | games | Game Engine Development |
| 355 | learn-55dd02e0 | awesome | Advanced | teen+ | web | Vert.x |
| 356 | learn-598efc2c | awesome | Advanced | teen+ | general | RxJava |
| 357 | learn-5daa78d3 | awesome | Advanced | teen+ | general | Audit Algorithms |
| 358 | learn-5e5c9cb1 | awesome | Advanced | teen+ | art | Apache Spark |
| 359 | learn-631d0b01 | awesome | Advanced | teen+ | general | Software Engineering for Machine Learning |
| 360 | learn-666aa764 | awesome | Advanced | teen+ | general | Natural Language Generation |
| 361 | learn-723d1d9b | awesome | Advanced | teen+ | web | WebGPU |
| 362 | learn-7494e14f | awesome | Advanced | teen+ | general | Ponyfills |
| 363 | learn-78c4641f | awesome | Advanced | teen+ | general | Haskell |
| 364 | learn-7aca8149 | awesome | Advanced | teen+ | general | Observables |
| 365 | learn-7b5a0c06 | awesome | Advanced | teen+ | general | Functional Programming |
| 366 | learn-7ed08f49 | awesome | Advanced | teen+ | general | Common Lisp |
| 367 | learn-85890561 | awesome | Advanced | teen+ | general | Vala |
| 368 | learn-8a2124fb | awesome | Advanced | teen+ | general | ClojureScript |
| 369 | learn-8b55a4ea | awesome | Advanced | teen+ | web | Seed |
| 370 | learn-93849c74 | awesome | Advanced | teen+ | general | PureScript |
| 371 | learn-93c7b8ed | awesome | Advanced | teen+ | general | XAI |
| 372 | learn-95dbfbfe | awesome | Advanced | teen+ | art | Hadoop |
| 373 | learn-9c151a58 | awesome | Advanced | teen+ | general | Asyncio |
| 374 | learn-9e615f09 | awesome | Advanced | teen+ | general | Computer Vision |
| 375 | learn-9ffd21af | awesome | Advanced | teen+ | web | Uno Platform |
| 376 | learn-a21a7245 | awesome | Advanced | teen+ | general | Crystal |
| 377 | learn-a93b975c | awesome | Advanced | teen+ | general | Theoretical Computer Science |
| 378 | learn-aacdfb2c | awesome | Advanced | teen+ | general | Groovy |
| 379 | learn-ad6a786a | awesome | Advanced | teen+ | general | Ada/SPARK |
| 380 | learn-b9a1985e | awesome | Advanced | teen+ | general | TensorFlow.js |
| 381 | learn-bb0122f9 | awesome | Advanced | teen+ | general | Fortran |
| 382 | learn-bf13977d | awesome | Advanced | teen+ | general | Deep Vision |
| 383 | learn-c2c4a263 | awesome | Advanced | teen+ | general | TensorFlow |
| 384 | learn-c2d06255 | awesome | Advanced | teen+ | web | WebAssembly |
| 385 | learn-ca8237ff | awesome | Advanced | teen+ | general | H2O |
| 386 | learn-d873c719 | awesome | Advanced | teen+ | general | Idris |
| 387 | learn-da850b4e | awesome | Advanced | teen+ | games | Game Production |
| 388 | learn-dbebd220 | awesome | Advanced | teen+ | general | Core ML Models |
| 389 | learn-dd0b5243 | awesome | Advanced | teen+ | art | Speech and Natural Language Processing |
| 390 | learn-de4ca268 | awesome | Advanced | teen+ | general | Machine Learning |
| 391 | learn-e1cf82ab | awesome | Advanced | teen+ | art | OpenGL |
| 392 | learn-e1f70867 | awesome | Advanced | teen+ | web | Scalability |
| 393 | learn-e50398cb | awesome | Advanced | teen+ | general | Julia |
| 394 | learn-e6d50f9b | awesome | Advanced | teen+ | general | Ansible |
| 395 | learn-e850fb9a | awesome | Advanced | teen+ | general | Pest |
| 396 | learn-ea219f5b | awesome | Advanced | teen+ | general | Scala |
| 397 | learn-ebbd2c3a | awesome | Advanced | teen+ | web | Cycle.js |
| 398 | learn-eef4ed36 | awesome | Advanced | teen+ | general | OCaml |
| 399 | learn-eef8c855 | awesome | Advanced | teen+ | general | Erlang |
| 400 | learn-f21dfe7f | awesome | Advanced | teen+ | art | Vulkan |
| 401 | learn-f715f931 | awesome | Advanced | teen+ | web | Yew |
