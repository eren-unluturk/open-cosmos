# Translation queue (kid-safe entries not yet translated into es/ar/hi/pt)

Regenerate with `python scripts/translate_queue.py`. **377 entries** still need es, ar, hi and pt for `title` and `desc`. Priority: CS Unplugged first, then Beginner, then Intermediate, then Advanced.

## Counts

| Source | Beginner | Intermediate | Advanced | Total |
|---|---|---|---|---|
| awesome | 0 | 258 | 65 | 323 |
| build-your-own-x | 0 | 36 | 18 | 54 |
| CS Unplugged | 0 | 0 | 0 | 0 |
| **All** | 0 | 294 | 83 | 377 |

## How to work through it
- **By hand (no API key):** add a module in `scripts/translation_content/` with `build()` returning `{entry id: {"title": {lang: ...}, "desc": {lang: ...}}}` for es, ar, hi, pt (see `kids_activities.py`), then run `python scripts/apply_translations.py` and the tests. Keep code and technical terms in English. They are labeled `ai_translated`.
- **With an API key:** `python scripts/translate.py --limit N` (kid-safe only, priority order, 5 requests at a time; add `--all` for everything).
- Still needs native-speaker checks for all four languages.

## Queue

| # | id | source | level | age | topic | title (en) |
|---|---|---|---|---|---|---|
| 1 | build-021ddad9 | build-your-own-x | Intermediate | teen+ | general | Writing a Link Checker |
| 2 | build-05969466 | build-your-own-x | Intermediate | teen+ | web | lets-build-express |
| 3 | build-15e24f81 | build-your-own-x | Intermediate | teen+ | games | How To Unity ARCore |
| 4 | build-16587794 | build-your-own-x | Intermediate | 11-13 | games | Build your own 8-Ball Pool game from scratch |
| 5 | build-1eefac4d | build-your-own-x | Intermediate | teen+ | general | A Neural Network in 11 lines of Python |
| 6 | build-25d276a6 | build-your-own-x | Intermediate | teen+ | games | Coding a Rogue/Nethack RPG in C |
| 7 | build-2785ade2 | build-your-own-x | Intermediate | teen+ | general | How to Augmented Reality AR Tutorial: ARKit Portal to the Upside Down |
| 8 | build-27f27e0a | build-your-own-x | Intermediate | teen+ | games | Roguelike Tutorial in Rust + tcod |
| 9 | build-28a71ea2 | build-your-own-x | Intermediate | teen+ | general | Continuous Integration System |
| 10 | build-361c58ea | build-your-own-x | Intermediate | teen+ | general | Writing a MiniTest Framework |
| 11 | build-4c870d39 | build-your-own-x | Intermediate | teen+ | art | Build your own 3D renderer |
| 12 | build-55f98526 | build-your-own-x | Intermediate | teen+ | web | Writing a URL Shortening Service |
| 13 | build-62aac5fc | build-your-own-x | Intermediate | teen+ | general | A Template Engine |
| 14 | build-6716814f | build-your-own-x | Intermediate | teen+ | games | Coding A Sudoku Solver in C |
| 15 | build-67cc0442 | build-your-own-x | Intermediate | teen+ | general | Neural Networks: Zero to Hero |
| 16 | build-6a17accb | build-your-own-x | Intermediate | teen+ | web | Building a frontend framework, from scratch, with components (templati |
| 17 | build-6d17c1f0 | build-your-own-x | Intermediate | teen+ | general | Lexical Scanning in Go |
| 18 | build-75ee0c25 | build-your-own-x | Intermediate | teen+ | games | AR Portal Tutorial with Unity |
| 19 | build-760f10e2 | build-your-own-x | Intermediate | teen+ | general | Tiny Package Manager: Learns how npm or Yarn works |
| 20 | build-7ae22b77 | build-your-own-x | Intermediate | teen+ | games | How to create a Dragon in Augmented Reality in Unity ARCore |
| 21 | build-961a5b5f | build-your-own-x | Intermediate | teen+ | games | Let's Make: Dangerous Dave |
| 22 | build-a11ba8c6 | build-your-own-x | Intermediate | teen+ | web | Build Your Own Module Bundler - Minipack |
| 23 | build-a6c99700 | build-your-own-x | Intermediate | teen+ | general | Building A Python-Based Search Engine |
| 24 | build-ab775371 | build-your-own-x | Intermediate | teen+ | general | JavaScript Algorithms and Data Structures |
| 25 | build-c0c5d580 | build-your-own-x | Intermediate | teen+ | general | mal - Make a Lisp |
| 26 | build-c238feec | build-your-own-x | Intermediate | teen+ | art | A 3D Modeller |
| 27 | build-c28cc666 | build-your-own-x | Intermediate | teen+ | general | JSON Decoding Algorithm |
| 28 | build-ccdcf9db | build-your-own-x | Intermediate | teen+ | web | How to create a real-world Node CLI app with Node |
| 29 | build-d12c8bbc | build-your-own-x | Intermediate | teen+ | games | Games With Go |
| 30 | build-d51d79db | build-your-own-x | Intermediate | teen+ | web | Neural Networks - The Nature of Code |
| 31 | build-d8acae03 | build-your-own-x | Intermediate | teen+ | general | Python Tutorial: Make Your Own Text Editor |
| 32 | build-e8ae0363 | build-your-own-x | Intermediate | teen+ | games | Learn Video Game Programming in C |
| 33 | build-f3e0da40 | build-your-own-x | Intermediate | teen+ | web | Write your own MVC from scratch in PHP |
| 34 | build-f9f9837c | build-your-own-x | Intermediate | teen+ | art | Rasterization: a Practical Implementation |
| 35 | build-fdaf1687 | build-your-own-x | Intermediate | teen+ | web | A DIY guide to build your own React |
| 36 | build-fdb2cd89 | build-your-own-x | Intermediate | teen+ | general | Learn how to write a hash table in C |
| 37 | learn-010606a9 | awesome | Intermediate | teen+ | general | Testing |
| 38 | learn-02282bb3 | awesome | Intermediate | teen+ | web | Sass |
| 39 | learn-02647a3f | awesome | Intermediate | teen+ | general | Speaking |
| 40 | learn-041e4cc2 | awesome | Intermediate | 11-13 | games | Godot |
| 41 | learn-059b8c49 | awesome | Intermediate | teen+ | general | JSON |
| 42 | learn-059eabcc | awesome | Intermediate | teen+ | web | Tiny JS |
| 43 | learn-05d31f6f | awesome | Intermediate | teen+ | web | Inspiration |
| 44 | learn-061273e2 | awesome | Intermediate | teen+ | general | Elixir Books |
| 45 | learn-0699cf70 | awesome | Intermediate | teen+ | web | ES6 Tools |
| 46 | learn-06b6370e | awesome | Intermediate | teen+ | web | WebExtensions |
| 47 | learn-07de4fa6 | awesome | Intermediate | teen+ | art | Audio Visualization |
| 48 | learn-0a0d36e1 | awesome | Intermediate | 11-13 | games | Game Development |
| 49 | learn-0a8d26e8 | awesome | Intermediate | teen+ | general | Java |
| 50 | learn-0b9fc4cb | awesome | Intermediate | teen+ | art | Product Design |
| 51 | learn-0bd65248 | awesome | Intermediate | 11-13 | art | Pixel Art |
| 52 | learn-0bfcf3f0 | awesome | Intermediate | teen+ | general | Data Science |
| 53 | learn-0d4bd10a | awesome | Intermediate | teen+ | web | Svelte |
| 54 | learn-0e4f10f0 | awesome | Intermediate | teen+ | web | lit |
| 55 | learn-0e81811d | awesome | Intermediate | teen+ | web | PageSpeed Metrics |
| 56 | learn-0ed171df | awesome | Intermediate | teen+ | web | Search Engine Optimization |
| 57 | learn-0fcd0421 | awesome | Intermediate | teen+ | general | Regex |
| 58 | learn-11bef6ff | awesome | Intermediate | 11-13 | games | GameMaker |
| 59 | learn-136ee9a2 | awesome | Intermediate | teen+ | web | Backbone |
| 60 | learn-13e0a239 | awesome | Intermediate | 11-13 | general | Awesome |
| 61 | learn-15c5debf | awesome | Intermediate | teen+ | web | WebXR |
| 62 | learn-15f5ae21 | awesome | Intermediate | teen+ | general | Tech Videos |
| 63 | learn-16d19b2f | awesome | Intermediate | teen+ | web | JavaScript |
| 64 | learn-16e4820d | awesome | Intermediate | teen+ | web | Sitecore |
| 65 | learn-17c1e9b6 | awesome | Intermediate | teen+ | web | Static Website Services |
| 66 | learn-18e73173 | awesome | Intermediate | teen+ | general | Education |
| 67 | learn-1980376c | awesome | Intermediate | teen+ | general | NLP with Ruby |
| 68 | learn-1b9d3696 | awesome | Intermediate | teen+ | general | D |
| 69 | learn-1bada5df | awesome | Intermediate | teen+ | general | Naming |
| 70 | learn-1ce410e7 | awesome | Intermediate | teen+ | general | Product Management |
| 71 | learn-1d430314 | awesome | Intermediate | teen+ | general | Software Engineering Blogs |
| 72 | learn-1e3f3205 | awesome | Intermediate | teen+ | web | Web Archiving |
| 73 | learn-201f2b16 | awesome | Intermediate | 11-13 | general | Python |
| 74 | learn-2026e8a8 | awesome | Intermediate | teen+ | general | Must Watch Talks |
| 75 | learn-210cc042 | awesome | Intermediate | teen+ | web | Must-Watch Talks |
| 76 | learn-228a79e5 | awesome | Intermediate | teen+ | web | Blazor |
| 77 | learn-2408990a | awesome | Intermediate | teen+ | web | Electron |
| 78 | learn-26da6b4a | awesome | Intermediate | teen+ | general | npm scripts |
| 79 | learn-27e0a052 | awesome | Intermediate | teen+ | web | PostCSS |
| 80 | learn-27ed50cc | awesome | Intermediate | teen+ | general | Elixir |
| 81 | learn-28b0f1df | awesome | Intermediate | teen+ | general | Talks |
| 82 | learn-290ae11a | awesome | Intermediate | teen+ | web | Drupal |
| 83 | learn-2aa562be | awesome | Intermediate | teen+ | web | Frameworks |
| 84 | learn-2ac59774 | awesome | Intermediate | teen+ | web | REST |
| 85 | learn-2c2fe965 | awesome | Intermediate | 11-13 | general | Education |
| 86 | learn-2d24b9c3 | awesome | Intermediate | teen+ | art | Open Source Photography |
| 87 | learn-2df92a72 | awesome | Intermediate | teen+ | web | Phalcon |
| 88 | learn-2e129b6d | awesome | Intermediate | teen+ | games | Game Remakes |
| 89 | learn-30949ba7 | awesome | Intermediate | teen+ | general | Dart |
| 90 | learn-312db5d1 | awesome | Intermediate | teen+ | web | Charting |
| 91 | learn-3172c479 | awesome | Intermediate | teen+ | art | Creative Technology |
| 92 | learn-319d0668 | awesome | Intermediate | teen+ | general | Plone |
| 93 | learn-32521322 | awesome | Intermediate | teen+ | general | CSV |
| 94 | learn-3281aaed | awesome | Intermediate | teen+ | general | AutoHotkey |
| 95 | learn-329f7c09 | awesome | Intermediate | teen+ | general | Unicode |
| 96 | learn-337572ad | awesome | Intermediate | teen+ | web | MDBootstrap |
| 97 | learn-35195ff0 | awesome | Intermediate | teen+ | general | Static Analysis & Code Quality |
| 98 | learn-362cd209 | awesome | Intermediate | teen+ | web | Web Performance Optimization |
| 99 | learn-36b92aaf | awesome | Intermediate | teen+ | web | React Hooks |
| 100 | learn-3947ef91 | awesome | Intermediate | teen+ | general | R Books |
| 101 | learn-3a9e5234 | awesome | Intermediate | teen+ | web | Node.js |
| 102 | learn-3b12be6a | awesome | Intermediate | teen+ | web | Less |
| 103 | learn-3bafd5fb | awesome | Intermediate | teen+ | art | TikZ |
| 104 | learn-3bf77272 | awesome | Intermediate | teen+ | web | Dojo Toolkit |
| 105 | learn-3e11113c | awesome | Intermediate | teen+ | web | CakePHP |
| 106 | learn-3f6c9d7d | awesome | Intermediate | teen+ | general | Typing |
| 107 | learn-3f9c6545 | awesome | Intermediate | 11-13 | web | Web Accessibility |
| 108 | learn-3f9ff83f | awesome | Intermediate | teen+ | general | Maintenance Modules |
| 109 | learn-410647e2 | awesome | Intermediate | teen+ | general | Elm |
| 110 | learn-4160a0f0 | awesome | Intermediate | teen+ | general | Kotlin |
| 111 | learn-4380890d | awesome | Intermediate | teen+ | web | Web Audio |
| 112 | learn-4552bded | awesome | Intermediate | teen+ | web | Vue.js |
| 113 | learn-45f3f83e | awesome | Intermediate | teen+ | general | Mad Science npm Packages |
| 114 | learn-4710560f | awesome | Intermediate | teen+ | general | Read the Docs |
| 115 | learn-474c52c7 | awesome | Intermediate | teen+ | general | J2ME |
| 116 | learn-4897ef29 | awesome | Intermediate | teen+ | general | Falsehood |
| 117 | learn-4a70f925 | awesome | Intermediate | teen+ | web | nginx |
| 118 | learn-4a78daa9 | awesome | Intermediate | teen+ | general | F# |
| 119 | learn-4ad1f621 | awesome | Intermediate | teen+ | web | Meteor |
| 120 | learn-4b1f8fcb | awesome | Intermediate | teen+ | art | Generative AI |
| 121 | learn-4bc3fbbe | awesome | Intermediate | teen+ | web | SAP Commerce |
| 122 | learn-4d89aca2 | awesome | Intermediate | teen+ | general | Code Points |
| 123 | learn-4e330ff3 | awesome | Intermediate | teen+ | art | Plotters |
| 124 | learn-4eadffdb | awesome | Intermediate | teen+ | web | FastAPI |
| 125 | learn-4f54d0f5 | awesome | Intermediate | teen+ | web | Fiber |
| 126 | learn-4f9e33c7 | awesome | Intermediate | teen+ | art | FFmpeg |
| 127 | learn-50397e3e | awesome | Intermediate | teen+ | art | Fonts |
| 128 | learn-50825303 | awesome | Intermediate | teen+ | general | Functional Programming |
| 129 | learn-50a51bf4 | awesome | Intermediate | teen+ | general | Mind Expanding Books |
| 130 | learn-512c2773 | awesome | Intermediate | teen+ | games | Game Boy Development |
| 131 | learn-51aa9181 | awesome | Intermediate | teen+ | general | CMake |
| 132 | learn-535ea0a4 | awesome | Intermediate | teen+ | web | iOS UI |
| 133 | learn-5382d6e0 | awesome | Intermediate | teen+ | general | Clojure |
| 134 | learn-55e210eb | awesome | Intermediate | teen+ | general | .NET |
| 135 | learn-560b0354 | awesome | Intermediate | 11-13 | general | Learning |
| 136 | learn-5a4a20ed | awesome | Intermediate | teen+ | web | Deno |
| 137 | learn-5a988e3b | awesome | Intermediate | teen+ | web | Amazon Web Services |
| 138 | learn-5c36a179 | awesome | Intermediate | 11-13 | games | Open Source Games |
| 139 | learn-5c9e6ecf | awesome | Intermediate | teen+ | general | ActionScript 3 |
| 140 | learn-5dd9f6ed | awesome | Intermediate | teen+ | web | Scriptable |
| 141 | learn-5e6c6370 | awesome | Intermediate | teen+ | art | Audiovisual |
| 142 | learn-5e7b747b | awesome | Intermediate | teen+ | web | Motion UI Design |
| 143 | learn-5ee234db | awesome | Intermediate | teen+ | web | Umbraco |
| 144 | learn-5f96924b | awesome | Intermediate | teen+ | web | Play1 Framework |
| 145 | learn-604e86a5 | awesome | Intermediate | teen+ | art | GIF |
| 146 | learn-63a967ca | awesome | Intermediate | 11-13 | general | Creative Coding |
| 147 | learn-65d62bbf | awesome | Intermediate | teen+ | web | Angular |
| 148 | learn-6690262b | awesome | Intermediate | teen+ | general | Low Code |
| 149 | learn-6764d0ed | awesome | Intermediate | teen+ | general | Promises |
| 150 | learn-6860996c | awesome | Intermediate | 11-13 | games | Flame |
| 151 | learn-68fd5d71 | awesome | Intermediate | teen+ | general | Composer |
| 152 | learn-69b930f2 | awesome | Intermediate | 11-13 | web | Web Animation |
| 153 | learn-6a6c2e20 | awesome | Intermediate | teen+ | web | Design and Development Guides |
| 154 | learn-6be895bc | awesome | Intermediate | teen+ | general | Hackathon |
| 155 | learn-6e132d82 | awesome | Intermediate | teen+ | web | Apache Wicket |
| 156 | learn-6fda3a6c | awesome | Intermediate | 11-13 | general | Lua |
| 157 | learn-70e1be9a | awesome | Intermediate | 11-13 | web | Flexbox |
| 158 | learn-756e951b | awesome | Intermediate | 11-13 | web | Canvas |
| 159 | learn-75da339d | awesome | Intermediate | teen+ | web | Slim |
| 160 | learn-76bea68c | awesome | Intermediate | teen+ | general | Competitive Programming |
| 161 | learn-76ebe071 | awesome | Intermediate | teen+ | web | Protips |
| 162 | learn-77e350a6 | awesome | Intermediate | teen+ | games | Babylon.js |
| 163 | learn-78dd1ce6 | awesome | Intermediate | teen+ | web | Wagtail |
| 164 | learn-795c0520 | awesome | Intermediate | teen+ | web | Vorpal |
| 165 | learn-7960c641 | awesome | Intermediate | teen+ | web | Web Typography |
| 166 | learn-7bff144d | awesome | Intermediate | teen+ | web | Symfony |
| 167 | learn-7c1b2e0a | awesome | Intermediate | teen+ | web | WebGL |
| 168 | learn-7f044f2f | awesome | Intermediate | teen+ | web | Selenium |
| 169 | learn-8147746d | awesome | Intermediate | teen+ | web | Browser Extensions |
| 170 | learn-815f486f | awesome | Intermediate | 11-13 | art | Colorful |
| 171 | learn-845d1d23 | awesome | Intermediate | teen+ | web | Frontend Development |
| 172 | learn-863391f5 | awesome | Intermediate | teen+ | general | Pascal |
| 173 | learn-870c785a | awesome | Intermediate | 11-13 | general | Esolangs |
| 174 | learn-8aaf5f49 | awesome | Intermediate | 11-13 | games | Chess |
| 175 | learn-8b2968ba | awesome | Intermediate | teen+ | general | Education |
| 176 | learn-8cc4faa3 | awesome | Intermediate | 11-13 | web | CSS |
| 177 | learn-9074c352 | awesome | Intermediate | teen+ | web | Text Editing |
| 178 | learn-908dae14 | awesome | Intermediate | teen+ | general | C/C++ |
| 179 | learn-909c3360 | awesome | Intermediate | 11-13 | general | Education |
| 180 | learn-90fb074f | awesome | Intermediate | teen+ | web | Framer |
| 181 | learn-912c59a5 | awesome | Intermediate | 11-13 | games | Gideros |
| 182 | learn-936d4682 | awesome | Intermediate | teen+ | web | React Native |
| 183 | learn-96619f6f | awesome | Intermediate | 11-13 | art | Data Visualization |
| 184 | learn-9aa8ebe3 | awesome | Intermediate | teen+ | general | AutoIt |
| 185 | learn-9b7dd79d | awesome | Intermediate | teen+ | web | Dash |
| 186 | learn-9b9b9adc | awesome | Intermediate | teen+ | general | Data Science |
| 187 | learn-9c58a9f5 | awesome | Intermediate | teen+ | web | choo |
| 188 | learn-a0ea5af6 | awesome | Intermediate | teen+ | web | Lumen |
| 189 | learn-a18cd8d2 | awesome | Intermediate | teen+ | web | Ionic Framework |
| 190 | learn-a1de233d | awesome | Intermediate | teen+ | web | Dropwizard |
| 191 | learn-a21c0b8a | awesome | Intermediate | teen+ | general | R |
| 192 | learn-a2a01b5f | awesome | Intermediate | teen+ | web | Payload |
| 193 | learn-a2a85129 | awesome | Intermediate | teen+ | web | Aurelia |
| 194 | learn-a30fd642 | awesome | Intermediate | 11-13 | art | Design Principles |
| 195 | learn-a34d892e | awesome | Intermediate | teen+ | web | Gulp |
| 196 | learn-a41a2cbe | awesome | Intermediate | teen+ | general | Open Source Society University |
| 197 | learn-a4d22b04 | awesome | Intermediate | teen+ | web | Userscripts |
| 198 | learn-a5a667f5 | awesome | Intermediate | 11-13 | general | Playgrounds |
| 199 | learn-a742688f | awesome | Intermediate | teen+ | web | Biological Visualizations |
| 200 | learn-a838865a | awesome | Intermediate | 11-13 | general | Algorithm Visualizations |
| 201 | learn-a8dc24fd | awesome | Intermediate | teen+ | art | VLC |
| 202 | learn-a9b68eb1 | awesome | Intermediate | teen+ | web | Android UI |
| 203 | learn-aa0200fd | awesome | Intermediate | teen+ | art | Music |
| 204 | learn-aa33d325 | awesome | Intermediate | 11-13 | general | Free Programming Books |
| 205 | learn-ab1cc51f | awesome | Intermediate | teen+ | web | Design systems |
| 206 | learn-ab2c219a | awesome | Intermediate | teen+ | web | Draft.js |
| 207 | learn-ab969ada | awesome | Intermediate | teen+ | web | Silverstripe CMS |
| 208 | learn-aba72944 | awesome | Intermediate | teen+ | general | Tips |
| 209 | learn-ac95d8c5 | awesome | Intermediate | teen+ | general | Rust |
| 210 | learn-aca21a9a | awesome | Intermediate | teen+ | general | Linguistics |
| 211 | learn-ad1072de | awesome | Intermediate | teen+ | web | D3 |
| 212 | learn-ad89662c | awesome | Intermediate | teen+ | web | Tips |
| 213 | learn-ae3f04e7 | awesome | Intermediate | teen+ | web | Web Tools |
| 214 | learn-b2a338f8 | awesome | Intermediate | 11-13 | general | Katas |
| 215 | learn-b373d1c2 | awesome | Intermediate | 11-13 | art | Screensavers |
| 216 | learn-b3c30fae | awesome | Intermediate | teen+ | general | Ruby |
| 217 | learn-b5af35c8 | awesome | Intermediate | teen+ | general | Node-RED |
| 218 | learn-b66eb4ad | awesome | Intermediate | teen+ | web | Cross-Platform |
| 219 | learn-b674d108 | awesome | Intermediate | teen+ | general | Swift |
| 220 | learn-b94bf5f9 | awesome | Intermediate | teen+ | web | Master CSS |
| 221 | learn-b9e65004 | awesome | Intermediate | 11-13 | general | Algorithms |
| 222 | learn-bb120595 | awesome | Intermediate | teen+ | general | Go Books |
| 223 | learn-bb91aa40 | awesome | Intermediate | teen+ | web | Useful .htaccess Snippets |
| 224 | learn-bccc5beb | awesome | Intermediate | teen+ | web | Emails |
| 225 | learn-bd1d4010 | awesome | Intermediate | teen+ | general | University Courses |
| 226 | learn-bdc65c6f | awesome | Intermediate | teen+ | general | Micro npm Packages |
| 227 | learn-be51c90e | awesome | Intermediate | teen+ | art | Stock Resources |
| 228 | learn-bfcea038 | awesome | Intermediate | teen+ | general | Pyramid |
| 229 | learn-c05b83f3 | awesome | Intermediate | 11-13 | general | Spanish |
| 230 | learn-c0b4c604 | awesome | Intermediate | teen+ | general | Flask |
| 231 | learn-c1486e86 | awesome | Intermediate | teen+ | general | QR Code |
| 232 | learn-c17ba638 | awesome | Intermediate | teen+ | web | Mobile Web Development |
| 233 | learn-c1897ebf | awesome | Intermediate | teen+ | web | Web Performance Budget |
| 234 | learn-c360eafa | awesome | Intermediate | teen+ | web | Progressive Enhancement |
| 235 | learn-c3f955b8 | awesome | Intermediate | teen+ | web | React |
| 236 | learn-c563507a | awesome | Intermediate | 11-13 | general | Learning |
| 237 | learn-c5f28ddc | awesome | Intermediate | teen+ | web | WordPress-Gatsby |
| 238 | learn-c6dd2618 | awesome | Intermediate | teen+ | web | Polymer |
| 239 | learn-c72fdd95 | awesome | Intermediate | teen+ | web | Reflex |
| 240 | learn-c83f83bc | awesome | Intermediate | teen+ | general | ESLint |
| 241 | learn-cab71370 | awesome | Intermediate | 11-13 | web | SVG |
| 242 | learn-cb0a8e44 | awesome | Intermediate | teen+ | general | ML with Ruby |
| 243 | learn-cb6c86c5 | awesome | Intermediate | teen+ | web | Storybook |
| 244 | learn-cba9ba60 | awesome | Intermediate | teen+ | web | Next.js |
| 245 | learn-cbe7c340 | awesome | Intermediate | teen+ | web | Magento 2 |
| 246 | learn-cc8c264b | awesome | Intermediate | teen+ | web | Progressive Web Apps |
| 247 | learn-cd095406 | awesome | Intermediate | teen+ | web | Visual Regression Testing |
| 248 | learn-cef56a91 | awesome | Intermediate | teen+ | web | Cordova |
| 249 | learn-cf448cc4 | awesome | Intermediate | teen+ | general | Book Authoring |
| 250 | learn-d15ace71 | awesome | Intermediate | teen+ | games | CHIP-8 |
| 251 | learn-d1d1f7ff | awesome | Intermediate | teen+ | general | npm |
| 252 | learn-d38bd96e | awesome | Intermediate | teen+ | web | Refinery CMS |
| 253 | learn-d41abc21 | awesome | Intermediate | teen+ | web | Ant Design |
| 254 | learn-d5386503 | awesome | Intermediate | teen+ | web | Textpattern |
| 255 | learn-d5b17289 | awesome | Intermediate | teen+ | web | Material-UI |
| 256 | learn-d672c131 | awesome | Intermediate | teen+ | web | Building Blocks for Web Apps |
| 257 | learn-d828206b | awesome | Intermediate | 11-13 | art | Icons |
| 258 | learn-d90cfcbb | awesome | Intermediate | teen+ | web | BEM |
| 259 | learn-daa2446b | awesome | Intermediate | teen+ | games | Haxe Game Development |
| 260 | learn-db5fb6b7 | awesome | Intermediate | teen+ | web | Browserify |
| 261 | learn-dbba4056 | awesome | Intermediate | teen+ | web | Playwright |
| 262 | learn-dcb5cdf5 | awesome | Intermediate | teen+ | general | Codeface |
| 263 | learn-de8e9f56 | awesome | Intermediate | teen+ | web | GraphQL |
| 264 | learn-e13a52bc | awesome | Intermediate | teen+ | web | Critical-Path Tools |
| 265 | learn-e27a486c | awesome | Intermediate | 11-13 | web | HTML5 |
| 266 | learn-e2d71c25 | awesome | Intermediate | teen+ | web | Capacitor |
| 267 | learn-e37b88c4 | awesome | Intermediate | teen+ | web | WP-CLI |
| 268 | learn-e3b96168 | awesome | Intermediate | teen+ | general | Go |
| 269 | learn-e44c8d6a | awesome | Intermediate | teen+ | general | Imba |
| 270 | learn-e855f3f3 | awesome | Intermediate | teen+ | general | ColdFusion |
| 271 | learn-e87f840f | awesome | Intermediate | teen+ | web | Marionette.js |
| 272 | learn-e8c9a498 | awesome | Intermediate | 11-13 | games | Construct 2 |
| 273 | learn-e980316d | awesome | Intermediate | teen+ | web | Inertia.js |
| 274 | learn-e9d4ee24 | awesome | Intermediate | teen+ | web | Ember |
| 275 | learn-ea7d5fde | awesome | Intermediate | teen+ | general | Perl |
| 276 | learn-eb35fbe3 | awesome | Intermediate | teen+ | web | Hyper |
| 277 | learn-eb89f448 | awesome | Intermediate | teen+ | web | Chrome DevTools |
| 278 | learn-ebcfca04 | awesome | Intermediate | teen+ | general | Standard Style |
| 279 | learn-ecc897b0 | awesome | Intermediate | teen+ | web | KnockoutJS |
| 280 | learn-eeb78cd4 | awesome | Intermediate | teen+ | web | Preact |
| 281 | learn-f0b42e1d | awesome | Intermediate | teen+ | games | Game Talks |
| 282 | learn-f2a21163 | awesome | Intermediate | 11-13 | web | Web Design |
| 283 | learn-f2aa26ad | awesome | Intermediate | teen+ | web | Material Design |
| 284 | learn-f3119b47 | awesome | Intermediate | teen+ | general | PHP |
| 285 | learn-f4e78a20 | awesome | Intermediate | teen+ | general | Conversational AI |
| 286 | learn-f5c4ed27 | awesome | Intermediate | teen+ | general | AVA |
| 287 | learn-f715f6ec | awesome | Intermediate | teen+ | web | Laravel |
| 288 | learn-f716942b | awesome | Intermediate | 11-13 | general | Education |
| 289 | learn-fa101958 | awesome | Intermediate | teen+ | games | libGDX |
| 290 | learn-fa128a35 | awesome | Intermediate | teen+ | web | Rails |
| 291 | learn-fbd2a0bc | awesome | Intermediate | teen+ | web | JAMstack |
| 292 | learn-fc038e95 | awesome | Intermediate | teen+ | web | Redux |
| 293 | learn-fc7650fc | awesome | Intermediate | 11-13 | general | Math |
| 294 | learn-fc98a49c | awesome | Intermediate | teen+ | games | PlayCanvas |
| 295 | build-0154ebfa | build-your-own-x | Advanced | teen+ | general | SlowTorch: Implementation of PyTorch from the ground up in 100% pure P |
| 296 | build-0dd2a748 | build-your-own-x | Advanced | teen+ | games | Reconstructing Cave Story |
| 297 | build-1b76c92d | build-your-own-x | Advanced | teen+ | general | Build a Deep Learning Library |
| 298 | build-1f1bc03a | build-your-own-x | Advanced | teen+ | general | A Large Language Model (LLM) |
| 299 | build-2156aefb | build-your-own-x | Advanced | teen+ | web | Building React From Scratch |
| 300 | build-28348eb1 | build-your-own-x | Advanced | teen+ | art | 3D Physics Engine Tutorial |
| 301 | build-2cf54114 | build-your-own-x | Advanced | teen+ | general | Optical Character Recognition (OCR) |
| 302 | build-514158f4 | build-your-own-x | Advanced | teen+ | art | Ray Tracing in One Weekend |
| 303 | build-5ab37fe3 | build-your-own-x | Advanced | teen+ | games | Make your own Game Engine |
| 304 | build-69566814 | build-your-own-x | Advanced | teen+ | general | Build Deep Learning From Scratch (reimplement PyTorch internals across |
| 305 | build-9ab4653e | build-your-own-x | Advanced | teen+ | general | RAG for Document Search |
| 306 | build-aeccd2f8 | build-your-own-x | Advanced | teen+ | art | How OpenGL works: software rendering in 500 lines of code |
| 307 | build-bcb475f9 | build-your-own-x | Advanced | teen+ | general | Creating JVM Language |
| 308 | build-d68ab5c2 | build-your-own-x | Advanced | teen+ | web | Building a Custom React Renderer |
| 309 | build-dbc6b593 | build-your-own-x | Advanced | teen+ | games | Remaking Cavestory in C++ |
| 310 | build-ebb0d512 | build-your-own-x | Advanced | teen+ | games | Chess Engine In C |
| 311 | build-f459bc96 | build-your-own-x | Advanced | teen+ | general | A Python Interpreter Written in Python |
| 312 | build-fb216e8e | build-your-own-x | Advanced | teen+ | general | Jonesforth |
| 313 | learn-01b8fcea | awesome | Advanced | teen+ | general | Scala Native |
| 314 | learn-06989e0f | awesome | Advanced | teen+ | web | Relay |
| 315 | learn-0db64ee0 | awesome | Advanced | teen+ | web | Frontend GIS |
| 316 | learn-122117c4 | awesome | Advanced | teen+ | web | Web Components |
| 317 | learn-131a52a2 | awesome | Advanced | teen+ | general | Question Answering |
| 318 | learn-1418a550 | awesome | Advanced | teen+ | general | Recursion Schemes |
| 319 | learn-171b13b5 | awesome | Advanced | teen+ | general | TensorFlow Lite |
| 320 | learn-18a80f99 | awesome | Advanced | teen+ | general | JAX |
| 321 | learn-1c4e452f | awesome | Advanced | teen+ | general | Q# |
| 322 | learn-21c37b3f | awesome | Advanced | teen+ | general | Empirical Software Engineering |
| 323 | learn-26554baf | awesome | Advanced | teen+ | general | Quantum Computing |
| 324 | learn-33d21ae1 | awesome | Advanced | teen+ | general | Papers |
| 325 | learn-3765ef2a | awesome | Advanced | teen+ | games | Game Datasets |
| 326 | learn-48ecfbb7 | awesome | Advanced | teen+ | general | Scientific Audio |
| 327 | learn-49089992 | awesome | Advanced | teen+ | web | Service Workers |
| 328 | learn-4f68305c | awesome | Advanced | teen+ | general | Deep Learning |
| 329 | learn-4fb0f569 | awesome | Advanced | teen+ | general | Coq |
| 330 | learn-50b06fb3 | awesome | Advanced | teen+ | games | Game Engine Development |
| 331 | learn-55dd02e0 | awesome | Advanced | teen+ | web | Vert.x |
| 332 | learn-598efc2c | awesome | Advanced | teen+ | general | RxJava |
| 333 | learn-5daa78d3 | awesome | Advanced | teen+ | general | Audit Algorithms |
| 334 | learn-5e5c9cb1 | awesome | Advanced | teen+ | art | Apache Spark |
| 335 | learn-631d0b01 | awesome | Advanced | teen+ | general | Software Engineering for Machine Learning |
| 336 | learn-666aa764 | awesome | Advanced | teen+ | general | Natural Language Generation |
| 337 | learn-723d1d9b | awesome | Advanced | teen+ | web | WebGPU |
| 338 | learn-7494e14f | awesome | Advanced | teen+ | general | Ponyfills |
| 339 | learn-78c4641f | awesome | Advanced | teen+ | general | Haskell |
| 340 | learn-7aca8149 | awesome | Advanced | teen+ | general | Observables |
| 341 | learn-7b5a0c06 | awesome | Advanced | teen+ | general | Functional Programming |
| 342 | learn-7ed08f49 | awesome | Advanced | teen+ | general | Common Lisp |
| 343 | learn-85890561 | awesome | Advanced | teen+ | general | Vala |
| 344 | learn-8a2124fb | awesome | Advanced | teen+ | general | ClojureScript |
| 345 | learn-8b55a4ea | awesome | Advanced | teen+ | web | Seed |
| 346 | learn-93849c74 | awesome | Advanced | teen+ | general | PureScript |
| 347 | learn-93c7b8ed | awesome | Advanced | teen+ | general | XAI |
| 348 | learn-95dbfbfe | awesome | Advanced | teen+ | art | Hadoop |
| 349 | learn-9c151a58 | awesome | Advanced | teen+ | general | Asyncio |
| 350 | learn-9e615f09 | awesome | Advanced | teen+ | general | Computer Vision |
| 351 | learn-9ffd21af | awesome | Advanced | teen+ | web | Uno Platform |
| 352 | learn-a21a7245 | awesome | Advanced | teen+ | general | Crystal |
| 353 | learn-a93b975c | awesome | Advanced | teen+ | general | Theoretical Computer Science |
| 354 | learn-aacdfb2c | awesome | Advanced | teen+ | general | Groovy |
| 355 | learn-ad6a786a | awesome | Advanced | teen+ | general | Ada/SPARK |
| 356 | learn-b9a1985e | awesome | Advanced | teen+ | general | TensorFlow.js |
| 357 | learn-bb0122f9 | awesome | Advanced | teen+ | general | Fortran |
| 358 | learn-bf13977d | awesome | Advanced | teen+ | general | Deep Vision |
| 359 | learn-c2c4a263 | awesome | Advanced | teen+ | general | TensorFlow |
| 360 | learn-c2d06255 | awesome | Advanced | teen+ | web | WebAssembly |
| 361 | learn-ca8237ff | awesome | Advanced | teen+ | general | H2O |
| 362 | learn-d873c719 | awesome | Advanced | teen+ | general | Idris |
| 363 | learn-da850b4e | awesome | Advanced | teen+ | games | Game Production |
| 364 | learn-dbebd220 | awesome | Advanced | teen+ | general | Core ML Models |
| 365 | learn-dd0b5243 | awesome | Advanced | teen+ | art | Speech and Natural Language Processing |
| 366 | learn-de4ca268 | awesome | Advanced | teen+ | general | Machine Learning |
| 367 | learn-e1cf82ab | awesome | Advanced | teen+ | art | OpenGL |
| 368 | learn-e1f70867 | awesome | Advanced | teen+ | web | Scalability |
| 369 | learn-e50398cb | awesome | Advanced | teen+ | general | Julia |
| 370 | learn-e6d50f9b | awesome | Advanced | teen+ | general | Ansible |
| 371 | learn-e850fb9a | awesome | Advanced | teen+ | general | Pest |
| 372 | learn-ea219f5b | awesome | Advanced | teen+ | general | Scala |
| 373 | learn-ebbd2c3a | awesome | Advanced | teen+ | web | Cycle.js |
| 374 | learn-eef4ed36 | awesome | Advanced | teen+ | general | OCaml |
| 375 | learn-eef8c855 | awesome | Advanced | teen+ | general | Erlang |
| 376 | learn-f21dfe7f | awesome | Advanced | teen+ | art | Vulkan |
| 377 | learn-f715f931 | awesome | Advanced | teen+ | web | Yew |
