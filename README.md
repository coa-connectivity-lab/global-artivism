# Movement, Water, Connection

Field illustration and GIS maps from the Côa Valley, Portugal. A coa-connectivity-lab contribution to [Global Artivism Month](https://globalartivism.ca), 1 November to 10 December 2026.

Live site: https://coa-connectivity-lab.github.io/global-artivism/

The site does two things: (i) it is the link for the "Share my art" submission on the Global Artivism Month participation form, and (ii) it hosts the open Côa call for participants during the month.

## Structure

```
index.html              single self-contained page (EN / PT / FR), no build step
img/                    rendered maps + illustration slots (see img/README.md)
data/field-sites.geojson field sites for the Leaflet map (Côa study area, non-sensitive only)
scripts/render_maps.py  renders img/map-*.png and data/field-sites.geojson
```

## Rerun the maps

The script reads the unzipped v6 data bundle ([data.gouv.fr](https://www.data.gouv.fr/datasets/coa-valley-eco-connectivity-v6)). Set `BUNDLE` at the top of the script to where you unzipped it, then:

```bash
conda run -n coa python scripts/render_maps.py
```

It needs rioxarray, geopandas and matplotlib.

## Add the illustrations

Drop scans into `img/` with the names listed in [img/README.md](img/README.md). The page picks them up automatically, no HTML edit needed. Credit any image not made by Linda in its caption.

## Text

English is the reference text. The Portuguese and French versions are drafts and need review before 6 October.

## Licence

Illustrations and text: CC BY-NC 4.0. Map data: Licence Ouverte 2.0 (Etalab), with underlying sources credited in the page footer. Code: MIT. See [LICENSE](LICENSE).
