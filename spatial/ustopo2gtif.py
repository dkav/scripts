"""Script to convert USGS Topo Maps to GeoTiff

Script extracts orthographic and/or topgraphy layers from USGS Topo
GeoPFDs. The cutline is derived from the neatline stored in the
metadata. A lossless (--lossless, -l) option will create a raster that
is compressed using the DEFLATE lossless compression.


"""

import argparse
import atexit
import os
import shutil
import tempfile

from osgeo import gdal, ogr, osr


BOTH = 'both'
ORTHO = 'ortho'
TOPO = 'topo'


def build_overview(ov_tiff):
    """Build tiff overviews."""

    print("Building overviews.")

    os.system(' '.join([
        'gdaladdo',
        '--config COMPRESS_OVERVIEW JPEG',
        '--config PHOTOMETRIC_OVERVIEW YCBCR',
        '--config INTERLEAVE_OVERVIEW PIXEL',
        '-r average',
        ov_tiff,
        '2 4 8 16']))


def extract_topo(topo_in, topo_warp_opts):
    """Extract topographic map layers from GeoPDF."""

    print("Extracting topographic map layers.")

    topo_out = ''.join([os.path.splitext(topo_in)[0], "_", TOPO,
                        ".tif"])

    gdal.SetConfigOption(
        'GDAL_PDF_LAYERS_OFF',
        'Map_Collar,'
        'Images,'
        'Map_Frame.PLSS,'
        'Map_Frame.Projection_and_Grids,'
        'Map_Frame.Terrain.Shaded_Relief')
    topo_in_ds = gdal.Open(topo_in)
    gdal.Warp(topo_out, topo_in_ds, options=topo_warp_opts)
    gdal.SetConfigOption('GDAL_PDF_LAYERS_OFF', None)
    topo_in_ds = None

    build_overview(topo_out)


def extract_ortho(ortho_in, ortho_warp_opts):
    """Extract ortographic map layer from GeoPDF."""

    print("Extracting orthographic map layer.")

    ortho_out = ''.join([os.path.splitext(ortho_in)[0], "_", ORTHO,
                         ".tif"])

    gdal.SetConfigOption('GDAL_PDF_LAYERS', 'Images.Orthoimage')
    ortho_in_ds = gdal.Open(ortho_in)
    gdal.Warp(ortho_out, ortho_in_ds, options=ortho_warp_opts)
    gdal.SetConfigOption('GDAL_PDF_LAYERS', None)
    ortho_in_ds = None

    build_overview(ortho_out)


def create_cutline_shpfile(cut_img):
    """Making cutline shapefile from neatline metadata."""

    cutline_fname = 'cutline.shp'

    cut_in_ds = gdal.Open(cut_img)
    cutline_shpfile = os.path.join(TMP_DIR, cutline_fname)

    prj = cut_in_ds.GetProjection()
    neatline_wkt = cut_in_ds.GetMetadataItem("NEATLINE")
    cut_in_ds = None

    out_srs = osr.SpatialReference(wkt=prj)
    nl_polygon = ogr.CreateGeometryFromWkt(neatline_wkt)

    driver = ogr.GetDriverByName('ESRI Shapefile')
    shp_ds = driver.CreateDataSource(cutline_shpfile)
    layer = shp_ds.CreateLayer('Cutline',
                               srs=out_srs,
                               geom_type=ogr.wkbPolygon)
    layer_def = layer.GetLayerDefn()

    feature_idx = 0
    feature = ogr.Feature(layer_def)
    feature.SetGeometry(nl_polygon)
    feature.SetFID(feature_idx)
    layer.CreateFeature(feature)
    shp_ds = None

    return cutline_shpfile


def main():
    """Convert USGS Topo to GeoTiff"""

    parser = argparse.ArgumentParser(description='USTopo2GTif')
    parser.add_argument('--extract', '-e',
                        choices=[BOTH, ORTHO, TOPO],
                        default='both')
    parser.add_argument('--lossless', '-l', action='store_true')
    parser.add_argument('filename', nargs='*')
    args = parser.parse_args()

    gdal.SetConfigOption('GDAL_PDF_BANDS', '3')
    warp_options = {
        "options": ['overwrite'],
        "format": "GTiff",
        "cropToCutline": True,
        "dstAlpha": True}

    if not args.lossless:
        warp_options.update({
            "creationOptions": ['compress=JPEG', 'JPEG_QUALITY=80']})
    else:
        warp_options.update({
            "creationOptions": ['compress=DEFLATE', 'PREDICTOR=2']})

    for geopdf in args.filename:
        print("")
        print(' '.join(["*** Processing ", geopdf, " ***"]))

        warp_options.update({"cutlineDSName": create_cutline_shpfile(geopdf)})

        if args.extract == BOTH:
            extract_ortho(geopdf, gdal.WarpOptions(**warp_options))
            print("")
            extract_topo(geopdf, gdal.WarpOptions(**warp_options))
        elif args.extract == ORTHO:
            extract_ortho(geopdf, gdal.WarpOptions(**warp_options))
        else:
            extract_topo(geopdf, gdal.WarpOptions(**warp_options))

    gdal.SetConfigOption('GDAL_PDF_BANDS', None)


def cleanup():
    """Cleanup on exit."""
    shutil.rmtree(TMP_DIR)


if __name__ == "__main__":
    TMP_DIR = tempfile.mkdtemp()
    atexit.register(cleanup)
    main()
