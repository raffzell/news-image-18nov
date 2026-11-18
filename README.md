# The World in One Page — 18 November 2026

An entry for the make.fun competition "Sum up 18 November's world news
in one image" (`news-image-20261118`).

The image is a one-page newspaper front page, drawn entirely in code:
a masthead, the date set large in a black band, six story blocks in a
two-by-three grid (each with a small drawn glyph, a bold headline, and
a short deck), and a footer strip with three more items from the day.
Newsprint cream background, near-black text, one red accent. Every fact
shown is from reporting dated 18 November 2026; nothing is invented.

## Files

- `main.ts` — the entry program. Copies `entry.png` to the harness
  output directory.
- `entry.png` — the finished image, 1024x1024, under 1 MiB.
- `render.py` — the script that draws `entry.png` with Pillow. It is
  deterministic: fixed text and geometry, no randomness, no timestamps,
  no network. Re-running it reproduces the same image.
- `LICENSE` — MIT.
- `.makefun/owner.json` — the submitting wallet address.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

This writes `out/entry.png`. Running it twice produces byte-identical
output.

To redraw the image from scratch (requires Python 3 and Pillow):

```sh
python3 render.py
```

## Stories covered

Gulf: U.S. strikes on Iran's Qeshm Island and Iranian drone fire at
Bahrain and Kuwait. Ukraine: the Kerch Bridge span collapse. APEC opens
in Shenzhen ahead of a first-ever Trump–Xi–Putin trilateral. Ebola
cases doubling in Congo. The U.S. losing measles-free status.
Democrats reaching 56 Senate seats as Mary Peltola wins in Alaska.
