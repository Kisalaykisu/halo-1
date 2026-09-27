# NORDLIGHT HALO 1

A concept marathon racing shoe with a carbon rim around the foam instead of a plate under it.

Interactive product page with a live 3D model (three.js), scroll teardown, specs, record run and materials.

NORDLIGHT is a fictional brand. HALO 1 is an original concept shoe.

Open `index.html` through a web server (or GitHub Pages) to view it.

## Design your own

The "+" swatch after the four colorways opens a designer: pick a color for the upper, foam, sole base, trim and laces (ten curated colors each, including the four colorways' own), or start from a colorway. Designs can be named and shared with **Copy link**:

```
?design=<upper>-<foam>-<base>-<trim>-<laces>&name=Kisalay%27s+Night+Run   (hex colors without #)
?cw=dune                                                                  (a preset colorway)
```

The palette lives in `PARTS` in `index.html`. The "Enter the draw" form shows the current design's name and colors.

## Find my size

In "Enter the draw", sizes can be shown as US men's, US women's, UK or EU (the toggle above the size picker). **Find my size** opens a size finder with two ways in:

- **Foot length:** heel to longest toe, in cm or inches (`10.6`, `10,6`, `10 5/8` all work).
- **Size you wear:** Nike, Adidas, ASICS, New Balance, Hoka, Brooks or On, in US men's, US women's, UK or EU.

HALO 1 is made for a foot of (US men's + 18) cm, with US women's = men's + 1.5 and UK = US men's − 1. A length within 1.5 mm of a size is that size. Anything between two sizes gets both: the smaller for racing, the larger for everyday comfort. The larger one is filled in by default, which matches the spec's "go up half a size". The answer fills in the size picker, and the size is kept in the link:

```
?size=9            (US men's; the draw form shows it in whatever sizing is chosen)
?size=9&sizing=eu  (sizes shown as EU; also usw for US women's, uk)
```

It combines with the design parameters, e.g. `?cw=dune&size=9`. The other brands' charts are in `BRANDS` in `index.html`.

## View on your floor (AR)

The hero's "View on your floor" button opens the shoe at real size (27 cm, US M9) in the selected colorway:

- **iPhone / iPad (Safari):** AR Quick Look. The page exports a USDZ from the loaded model on tap.
- **Android:** Scene Viewer, using the prebuilt `ar/halo1-<colorway>.glb` files.
- **Desktop:** a QR code that opens the page, with the same colorway, on a phone.

A custom design shows exactly on iPhone/iPad. Android can only open the prebuilt preset files, so a custom design opens as the closest preset, and the page says so before launching. The desktop QR code carries the custom design to the phone.

After changing or adding a colorway in `index.html`, rebuild the Android files with `python3 tools/build_ar_models.py`.
