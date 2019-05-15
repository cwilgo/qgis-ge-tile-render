QGIS Tile Rendering Script
==========================

This is a quick (and dirty in its current state) script that renders a layer as a set of TIFF image files. Originally it was written to create a Google Earth layer using tile images, since one monolithic image doesn't work very well with Google Earth. It also makes it easier to host the images on a web server, allowing the KML file to be quickly downloaded or sent to others.

The next step is to convert this script into a proper QGIS plugin, allowing the user to configure the parameters using a UI rather than editing the script.