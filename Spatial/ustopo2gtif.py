"""Script to convert USGS Topo Maps to GeoTiff

Script extracts orthographic and/or topgraphy layers from USGS Topo
GeoPFDs. The cutline is derived from the neatline stored in the
metadata. A lossy (--lossy, -l) option will create a raster that
is compressed in a JPEG format without an alpha layer. This can
create edge issues which are visible when including overlapping
rasters in the same map.


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

CUTLINE_FNAME = 'cutline.shp'

GWARP_BASE = (' '.join([
    'gdalwarp',
    '-of GTiff',
    '-overwrite',
    '-crop_to_cutline',
    '--config GDAL_PDF_BANDS 3']))


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


def extract_topo(tinput_cmd, topo_path):
    """Extract topographic map layers from GeoPDF."""

    print("Extracting topographic map layers.")

    topo_tiff = ''.join([topo_path, '_topo.tif'])
    ex_topo_cmd = (''.join([
        tinput_cmd,
        ' --config GDAL_PDF_LAYERS_OFF ',
        'Map_Collar,',
        'Images,',
        'Map_Frame.Projection_and_Grids,',
        'Map_Frame.Terrain.Shaded_Relief ',
        topo_tiff]))
    os.system(ex_topo_cmd)
    build_overview(topo_tiff)


def extract_ortho(oinput_cmd, ortho_path):
    """Extract ortographic map layer from GeoPDF."""

    print("Extracting orthographic map layer.")

    ortho_tiff = ''.join([ortho_path, '_ortho.tif'])
    ex_ortho_cmd = (''.join([
        oinput_cmd,
        '--config GDAL_PDF_LAYERS ',
        'Images.Orthoimage ',
        ortho_tiff]))
    os.system(ex_ortho_cmd)
    build_overview(ortho_tiff)


def create_cutline_shpfile(img_file):
    """Making cutline shapefile from neatline metadata."""

    cutline_shpfile = os.path.join(TMP_DIR, CUTLINE_FNAME)

    in_img = gdal.Open(img_file)
    prj = in_img.GetProjection()
    neatline_wkt = in_img.GetMetadataItem("NEATLINE")
    in_img = None

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
    shp_ds.Destroy()

    return cutline_shpfile


def main():
    """Convert USGS Topo to GeoTiff"""

    parser = argparse.ArgumentParser(description='USTopo2GTif')
    parser.add_argument('--extract', '-e',
                        choices=[BOTH, ORTHO, TOPO],
                        default='both')
    parser.add_argument('--lossy', '-l', action='store_true')
    parser.add_argument('filename', nargs='*')
    args = parser.parse_args()

    if args.lossy:
        gdal_base_cmd = (' '.join([
            GWARP_BASE,
            '-co compress=JPEG'
            '-co PHOTOMETRIC=YCBCR']))
    else:
        gdal_base_cmd = ' '.join([
            GWARP_BASE,
            '-dstalpha',
            '-co compress=DEFLATE'])

    for geopdf in args.filename:
        print("")
        print(' '.join(["*** Processing ", geopdf, " ***"]))

        out_path = os.path.splitext(geopdf)[0]
        cutline_file = create_cutline_shpfile(geopdf)

        gdal_cmd = (' '.join([
            gdal_base_cmd,
            '-cutline', cutline_file,
            geopdf]))

        if args.extract == BOTH:
            extract_ortho(gdal_cmd, out_path)
            print("")
            extract_topo(gdal_cmd, out_path)
        elif args.extract == ORTHO:
            extract_ortho(gdal_cmd, out_path)
        else:
            extract_topo(gdal_cmd, out_path)


def cleanup():
    """Cleanup on exit."""
    shutil.rmtree(TMP_DIR)


if __name__ == "__main__":
    try:
        TMP_DIR = tempfile.mkdtemp()
    finally:
        print("Failed to create temp directory")
        exit()

    atexit.register(cleanup)
    main()
