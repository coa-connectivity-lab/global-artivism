"""Render the three Côa connectivity maps as clean images for the website,
and export the non-sensitive field sites to GeoJSON for the Leaflet map.

Run from the repo root:  conda run -n coa python scripts/render_maps.py
"""
from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import rioxarray

# Unzipped v6 data bundle (data.gouv.fr, Etalab 2.0)
BUNDLE = Path("/home/linda/Documents/myData/coa-eco-connectivity-data-v6/research/eco-connectivity")
RASTERS = BUNDLE / "output" / "rasters"
PROCESSED = BUNDLE / "data" / "processed"
OUT = Path(__file__).resolve().parent.parent

MAPS = {
    "movement": "land_normalized_current.tif",
    "water": "water_normalized_current.tif",
    "connection": "multispecies_mean_connectivity.tif",
}

# Côa river, reprojected to the raster CRS (EPSG:3035)
river = gpd.read_file(PROCESSED / "study_area.gpkg", layer="coa_river").to_crs(3035)

for name, tif in MAPS.items():
    da = rioxarray.open_rasterio(RASTERS / tif, masked=True).squeeze()
    xmin, ymin, xmax, ymax = da.rio.bounds()

    fig, ax = plt.subplots(figsize=(8, 8 * (ymax - ymin) / (xmax - xmin)), dpi=200)
    lo, hi = da.quantile([0.02, 0.98]).values
    ax.imshow(da.values, extent=(xmin, xmax, ymin, ymax), cmap="RdYlBu_r", vmin=lo, vmax=hi)
    river.plot(ax=ax, color="#10233f", linewidth=1.2)

    # 10 km scale bar and north arrow, bottom right
    x0, y0 = xmax - 14000, ymin + 3000
    ax.plot([x0, x0 + 10000], [y0, y0], color="#10233f", linewidth=3)
    ax.text(x0 + 5000, y0 + 1200, "10 km", ha="center", fontsize=8, color="#10233f")
    ax.annotate("N", xy=(xmax - 3000, ymin + 12000), xytext=(xmax - 3000, ymin + 7000),
                ha="center", fontsize=9, color="#10233f",
                arrowprops=dict(arrowstyle="-|>", color="#10233f"))

    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_axis_off()
    fig.savefig(OUT / "img" / f"map-{name}.png", bbox_inches="tight", pad_inches=0.05,
                facecolor="white")
    plt.close(fig)
    print("wrote", f"img/map-{name}.png")

# Field sites: Côa study area only, drop anything flagged sensitive, one point per site
sites = gpd.read_file(PROCESSED / "field_observations.gpkg", layer="visited_sites")
sites = sites[sites["in_study_area"].astype(bool) & ~sites["sensitive"].astype(bool)]
sites = sites.drop_duplicates("site_name")
sites = sites[["site_name", "date_and_time", "geometry"]].to_crs(4326)
sites["date"] = sites.pop("date_and_time").astype(str).str[:10]
sites.to_file(OUT / "data" / "field-sites.geojson", driver="GeoJSON")
print("wrote", len(sites), "sites to data/field-sites.geojson")
