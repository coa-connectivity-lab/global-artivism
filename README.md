# Movement, Water, Connection

Field illustration and GIS maps from the Côa Valley, Portugal. A coa-connectivity-lab contribution to [Global Artivism Month](https://globalartivism.ca), 1 November to 10 December 2026.

Live site: https://coa-connectivity-lab.github.io/global-artivism/

The site does two things: (i) it is the link for the "Share my art" submission on the Global Artivism Month participation form, and (ii) it hosted the Côa call for participants, which closed on 23 October 2026, and carries the month's prompts and round-ups.

## Illustration method

The page's "New animals in an old line" series draws the European rabbit, the European wildcat and the Mediterranean pond turtle in the fine-line style of the Côa Valley's Iron Age engravings. The method (study the line, study the animal, reduce to a profile, cut the line, caption honestly, pair with evidence) follows Section 8 of the preprint:

Angulo Lopez, L. (2026). *Rabbits, wildcats, pond turtles and a river that stayed: a synthesis and research agenda for trophic and hydrological rewilding in the Greater Côa Valley, Portugal*. Preprint v0.1, Zenodo. <https://zenodo.org/records/22997241>

Source files (article, PDF, reading list): <https://github.com/coa-connectivity-lab/Solo-field-illustrator-project-for-Rewilding-Portugal/tree/main/research/rewilding-dynamics>

## Structure

```
index.html              single self-contained page (EN / PT / ES / FR); link a language with ?lang=es, no build step
img/                    rendered maps + illustration slots (see img/README.md)
data/field-sites.geojson field sites for the Leaflet map (Côa study area, non-sensitive only)
scripts/render_maps.py  renders img/map-*.png and data/field-sites.geojson
scripts/digital_plates.py draws the digital plate studies (rabbit, wildcat, pond turtle)
scripts/digital_landscapes.py draws the three landscape studies (Movement, Water, Connection)
```

The two release screening maps in "Supporting studies" (`img/release-candidates-*.png`) are made by `research/rewilding-dynamics/scripts/release_candidates.py` in the source repo, from the v6 bundle, ESA WorldCover 2021, JRC Global Surface Water 2021 and GBIF records generalised to 5 km.

## Rerun the maps

The script reads the unzipped v6 data bundle ([data.gouv.fr](https://www.data.gouv.fr/datasets/coa-valley-eco-connectivity-v6)). Set `BUNDLE` at the top of the script to where you unzipped it, then:

```bash
conda run -n coa python scripts/render_maps.py
```

It needs rioxarray, geopandas and matplotlib.

## Redraw the digital plate studies

`scripts/digital_plates.py` draws the European rabbit, the European wildcat and the Mediterranean pond turtle as rough burnt sienna lines on a greyscale schist surface, after the Iron Age fine-line engravings of the Côa (preprint §8.2-8.3). The stone is generated, not photographed: foliation and cracks run NNE-SSW and the surface is pitted, as on the Côa panels. Each plate keeps one diagnostic feature (the rabbit's ears and short tail, the wildcat's blunt ringed tail, the turtle's low shell and striped neck) and is captioned as a new work, not an ancient motif.

```bash
conda run -n coa python scripts/digital_plates.py
```

It writes `img/digital-studies/digital-study-plate-*.jpg` (1600 x 2000 px, 4:5) and needs numpy, scipy, shapely and Pillow. The Exo 2 caption font (SIL OFL) is downloaded on first run. The Global Artivism Month logo is not in this repo: to add it to the caption band, save the white logo from the GAM comms kit as `img/gam-logo-white.png`. The drawings are seeded, so a rerun gives the same plates.

`scripts/digital_landscapes.py` uses the same surface, line and colour for the three landscape plates: i. Movement (Vale Carapito: horses, Tauros cattle, a wolf, fishbone trees), ii. Water (Paul de Toirões: open water, reeds, a heron and ducks, old drainage ditches fading into the marsh) and iii. Connection (the Côa gorge: stratified walls, the free-flowing river, a rock panel, terraces, a walker and a vulture). Run it the same way; it writes `img/digital-studies/digital-study-{movement,water,connection}.jpg`, which the page shows as `img/movement.jpg`, `img/water.jpg` and `img/connection.jpg`.

These are digital studies. The plates themselves are cut by hand (preprint §8.3, step iv).

AI assistance: the script was written with Claude (Anthropic) from Linda's method and art direction, and reviewed by Linda.

## Add the illustrations

Drop scans into `img/` with the names listed in [img/README.md](img/README.md). The page picks them up automatically, no HTML edit needed. Credit any image not made by Linda in its caption.

## Text

English is the reference text. The Portuguese, Spanish and French versions are drafts and need review before 6 October.

## Licence

Illustrations and text: CC BY-NC 4.0. Map data: Licence Ouverte 2.0 (Etalab), with underlying sources credited in the page footer. Code: MIT. See [LICENSE](LICENSE).
