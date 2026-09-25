# NORDLIGHT HALO 1

A concept marathon racing shoe with a carbon rim around the foam instead of a plate under it.

Interactive product page with a live 3D model (three.js), scroll teardown, specs, record run and materials.

NORDLIGHT is a fictional brand. HALO 1 is an original concept shoe.

Open `index.html` through a web server (or GitHub Pages) to view it.

## View on your floor (AR)

The hero's "View on your floor" button opens the shoe at real size (27 cm, US M9) in the selected colorway:

- **iPhone / iPad (Safari):** AR Quick Look. The page exports a USDZ from the loaded model on tap.
- **Android:** Scene Viewer, using the prebuilt `ar/halo1-<colorway>.glb` files.
- **Desktop:** a QR code that opens the page, with the same colorway, on a phone.

After changing or adding a colorway in `index.html`, rebuild the Android files with `python3 tools/build_ar_models.py`.
