# QGIS Tile Rendering Script

# Parameters:
dryRun = False
makeKML = True
dirOut = "/storage/Archive/Maps/AviSlope/ge/tiles/"
fileExt = ".tif"
scale = 0.5
xTileCount = -1
yTileCount = -1
maxWidth = 1024
maxHeight = 1024
filterMinValue = 21
filename_append = ""
opts = ["COMPRESS=LZW"]
#opts = ["COMPRESS=JPEG", "JPEG_QUALTIY=75"]
#opts = ["COMPRESS=DEFLATE", "PREDICTOR=2", "ZLEVEL=9"]

for layer in iface.mapCanvas().layers():
    extent = layer.extent()
    renderer = layer.renderer()
    provider = layer.dataProvider()
    pipe = QgsRasterPipe()
    pipe.set(provider.clone())
    pipe.set(renderer.clone())
    if xTileCount <= 0:
        xTileCount = round(layer.width() * scale / maxWidth)
    if yTileCount <= 0:
        yTileCount = round(layer.height() * scale / maxHeight)
    if xTileCount <= 0:
        xTileCount = 1
    if yTileCount <= 0:
        yTileCount = 1
#    width = layer.width() * scale / xTileCount
#    height = layer.height() * scale / yTileCount
    width = maxWidth
    height = maxHeight
#    if width > maxWidth:
#        factor = maxWidth / width
#        width = width * factor
#        height = height * factor
#    if height > maxHeight:
#        factor = maxHeight / height
#        width = width * factor
#        height = height * factor
    width = round(width)
    height = round(height)
    print("Tiles: " + str(xTileCount * yTileCount) + ", Grid: " + str(xTileCount) + " x " + str(yTileCount))

    tileWidth = extent.width() / xTileCount
    tileHeight = extent.height() / yTileCount
    nCount = 0
    for nXTile in range(0, xTileCount):
        for nYTile in range(0, yTileCount):
            nCount = nCount + 1
            tileExtent = layer.extent()
            tileExtent.setXMinimum(extent.xMinimum() + nXTile * tileWidth)
            tileExtent.setXMaximum(tileExtent.xMinimum() + tileWidth)
            tileExtent.setYMinimum(extent.yMinimum() + nYTile * tileHeight)
            tileExtent.setYMaximum(tileExtent.yMinimum() + tileHeight)
            stats = provider.bandStatistics(1, QgsRasterBandStats.All, tileExtent, 0)
            layerName = layer.name() + filename_append
            #outPath = dirOut + layer.name()[-4:] + filename_append
            if xTileCount > 1:
                layerName = layerName + "_" + str(nXTile)
            if yTileCount > 1:
                layerName = layerName + "_" + str(nYTile)
            outPath = dirOut + layerName + fileExt
            if stats.maximumValue > filterMinValue:
                filewriter = QgsRasterFileWriter(outPath)
                filewriter.setCreateOptions(opts)
                print(str(nCount) + "/" + str(xTileCount*yTileCount) + ": Exporting File: " + outPath + ", " + str(width) + " x " + str(height) + ", min=" + str(stats.minimumValue) + " max=" + str(stats.maximumValue))
                #print("   " + layer.name()[-4:])
                if not dryRun:
                    filewriter.writeRaster(pipe, width, height, tileExtent, layer.crs())
                if makeKML:
                    f = open(dirOut + layerName + ".kml", 'wt')
                    f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
                    f.write("<kml xmlns=\"http://www.opengis.net/kml/2.2\" xmlns:gx=\"http://www.google.com/kml/ext/2.2\" xmlns:kml=\"http://www.opengis.net/kml/2.2\" xmlns:atom=\"http://www.w3.org/2005/Atom\">\n")
                    f.write("<GroundOverlay>\n")
                    f.write("\t<name>" + layerName + "</name>\n")
                    f.write("\t<color>73ffffff</color>\n")
                    f.write("\t<Icon>\n")
                    f.write("\t\t<href>" + outPath + "</href>\n")
                    f.write("\t\t<viewBoundScale>0.75</viewBoundScale>\n")
                    f.write("\t</Icon>\n")
                    f.write("\t<LatLonBox>\n")
                    f.write("\t\t<north>" + str(tileExtent.yMaximum()) + "</north>\n")
                    f.write("\t\t<south>" + str(tileExtent.yMinimum()) + "</south>\n")
                    f.write("\t\t<east>" + str(tileExtent.xMaximum()) + "</east>\n")
                    f.write("\t\t<west>" + str(tileExtent.xMinimum()) + "</west>\n")
                    f.write("\t</LatLonBox>\n")
                    f.write("</GroundOverlay>\n")
                    f.write("</kml>\n")
                    f.close()
            else:
                print(str(nCount) + "/" + str(xTileCount*yTileCount) + ": Skipped File: " + outPath)
#    #outPath = dirOut + layer.name() + filename_append + ".tif"
#    outPath = dirOut + layer.name()[-4:] + filename_append + fileExt
#    filewriter = QgsRasterFileWriter(outPath)
#    filewriter.setCreateOptions(opts)
#    print("Exporting File: " + outPath + " " + str(width) + " x " + str(height))
#    #print("   " + layer.name()[-4:])
#    if not dryRun:
#        filewriter.writeRaster(pipe, width, height, extent, layer.crs())
print("Done.")
