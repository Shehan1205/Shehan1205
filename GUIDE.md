# How to use and edit your new profile

Everything on the profile comes from ONE file: `profile.json`.
You change that file, run one command, and the whole page (README + all animated images) is rebuilt.

```
python build.py
```

No packages needed (just Python 3.8+). Then commit and push.

---

## 1. First-time setup (put it on GitHub)

Your profile repo is `https://github.com/Shehan1205/Shehan1205`.

1. Delete the old files in that repo (old `README.md`, old `assets/` folder).
2. Copy everything from this folder into the repo root:
   `README.md`, `assets/`, `profile.json`, `build.py`, `tools/`, `.github/`, `GUIDE.md`
3. Commit and push:
   ```
   git add .
   git commit -m "New animated profile"
   git push
   ```
4. Turn on the snake animation (one time):
   - Open the repo on GitHub -> **Actions** tab -> **Generate snake animation** -> **Run workflow**.
   - Wait about a minute. It creates an `output` branch with the snake images. The snake in the README shows up after that.
   - If Actions asks for permission: repo **Settings -> Actions -> General -> Workflow permissions -> Read and write**.

If you do not want the snake, delete the `.github` folder and remove the `<picture>...</picture>` block in `build.py` (search for "snake").

GitHub can cache images for a minute or two. Refresh after a bit.

---

## 2. ADD new things (edit `profile.json`)

### Add a technology
Find the group in `"tech"` and add the name. Example:
```json
{ "group": "Data & Tools", "items": ["MySQL", "PostgreSQL", "Redis", "Git"] }
```
It gets its brand colour automatically if it is known (Redis, Laravel, Go, Kotlin, Tailwind, Vue, Angular, Linux, GraphQL and more are built in). Unknown names get a purple dot. To set a colour, add one line to `TECH_COLORS` near the top of `build.py`.
To add a whole new scrolling row, add a new `{ "group": "...", "items": [...] }` block.

### Add a project
Add a block to `"projects"` (keep names short, under about 30 characters):
```json
{
  "name": "My New App",
  "status": "In progress",
  "description": "One or two sentences about it.",
  "tags": ["React", "Node.js", "MongoDB"]
}
```
Cards sit two per row and the numbers (01, 02, 03...) update by themselves.

### Add a social link or badge
Add to `"links"`:
```json
{ "label": "LinkedIn", "url": "https://linkedin.com/in/yourname", "color": "0A66C2", "logo": "linkedin" }
```
`logo` is any name from simpleicons.org (github, facebook, linkedin, instagram, youtube, x...). Leave it `""` for no icon. It appears in both badge rows.

### Add a line to the typing animation
Add a sentence to `"typing_lines"` (keep it under about 40 characters). The banner loops through all of them.

### Add a console command
Add to `"console"`:
```json
{ "cmd": "location", "out": "Sri Lanka" }
```

### Add a focus row, interest or fact
`"focus"`, `"interests"`, `"about"` are plain text. Add or edit them the same way.

### Change the photo
```
pip install pillow
python tools/prepare_photo.py my-new-photo.jpg --cx 500 --cy 700 --size 740
python build.py
```
`--cx --cy --size` aim the square crop at your face (centre x, centre y and size, in pixels of the original photo). Try a few values until your face is centred.

### Change the name, role, company, location
Top of `profile.json` (`name`, `first_name`, `last_name`, `role`, `company`, `building`, `location`).

---

## 3. REMOVE things

Delete the item from `profile.json`, then run `python build.py`.

| To remove | Delete this from `profile.json` |
|:--|:--|
| A technology | its name inside `"items"` |
| A whole tech row | the whole `{ "group": ..., "items": ... }` block |
| A project | its whole `{ ... }` block inside `"projects"` |
| A social badge | its `{ ... }` block inside `"links"` |
| A typing line | the line inside `"typing_lines"` |
| A floating chip on the banner | the entry inside `"floating_chips"` |
| A console command | its block inside `"console"` |
| A focus row | its block inside `"focus"` |

Remember JSON rules: commas between items, **no comma after the last item**, double quotes only.

### Remove a whole section
Open `build.py`, go to `def build_readme()` and delete the section you do not want (each section starts with a line like `{h("projects", "Featured projects")}`) together with the content under it. Run `python build.py`. The section numbers in the headers are set near the bottom in `main()`; renumber there if you want.

### Remove the third-party stats cards
In `build_readme()` delete the `<img ... github-readme-stats ...>`, `streak-stats` and `activity-graph` lines. These are external services and can be slow or down sometimes; that is not a problem with your files.

---

## 4. Good to know
- `README.md` and everything in `assets/*.svg` are **generated**. If you edit them by hand, the next `python build.py` overwrites your edits. Edit `profile.json` instead (or `build.py` for layout and design changes).
- Colours and fonts are at the top of `build.py` (`CYAN`, `VIOLET`, `PINK`, `BG`...). Change them once and every image follows.
- Animation speeds are the `dur="..."` values inside `build.py` (bigger number = slower).
- Preview locally: open `README.md` in VS Code preview, or open any `assets/*.svg` in a browser to see its animation.
