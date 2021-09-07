from fiji.plugin.btrackmate.visualization.hyperstack import HyperStackDisplayer
from fiji.plugin.btrackmate.io import TmXmlReader
from fiji.plugin.btrackmate import Logger
from fiji.plugin.btrackmate import Settings
from fiji.plugin.btrackmate import SelectionModel
from fiji.plugin.btrackmate.gui.displaysettings import DisplaySettings
from fiji.plugin.btrackmate.providers import DetectorProvider
from fiji.plugin.btrackmate.providers import TrackerProvider
from fiji.plugin.btrackmate.providers import SpotAnalyzerProvider
from fiji.plugin.btrackmate.providers import EdgeAnalyzerProvider
from fiji.plugin.btrackmate.providers import TrackAnalyzerProvider
from fiji.plugin.btrackmate.providers import SpotMorphologyAnalyzerProvider;
from java.io import File
from fiji.plugin.btrackmate.io.TmXmlKeys import SETTINGS_ELEMENT_KEY;
from fiji.plugin.btrackmate.io.TmXmlKeys import IMAGE_ELEMENT_KEY;
from fiji.plugin.trackmate.io.TmXmlKeys import IMAGE_FILENAME_ATTRIBUTE_NAME;
from fiji.plugin.trackmate.io.TmXmlKeys import IMAGE_FOLDER_ATTRIBUTE_NAME ;
from fiji.plugin.btrackmate.io.TmXmlKeys import DISPLAY_SETTINGS_ELEMENT_KEY;
from org.jdom2.input import SAXBuilder;
from fiji.plugin.btrackmate.gui.displaysettings import DisplaySettingsIO;
from fiji.plugin.btrackmate.TrackMatePlugIn import localcreateSettings;
from  ij import IJ;

import sys


#----------------
# Setup variables
#----------------

# Put here the path to the TrackMate file you want to load
file = File('/Users/aimachine/Track_Analysis/113B_Day3/DUP_C3-20210122_113B_N1BcatTOM_day3_region3_each10min_zoom08_40x_FINAL.xml')

# We have to feed a logger to the reader.
logger = Logger.IJ_LOGGER

#-------------------
# Instantiate reader
#-------------------

reader = TmXmlReader(file)
if not reader.isReadingOk():
    sys.exit(reader.getErrorMessage())
#-----------------
# Get a full model
#-----------------

# This will return a fully working model, with everything
# stored in the file. Missing fields (e.g. tracks) will be
# null or None in python
model = reader.getModel()
# model is a fiji.plugin.trackmate.Model

# You might want to access only separate parts of the
# model.

spots = model.getSpots()
# spots is a fiji.plugin.trackmate.SpotCollection



# If you want to get the tracks, it is a bit trickier.
# Internally, the tracks are stored as a huge mathematical
# simple graph, which is what you retrieve from the file.
# There are methods to rebuild the actual tracks, taking
# into account for everything, but frankly, if you want to
# do that it is simpler to go through the model:

trackIDs = model.getTrackModel().trackIDs(True) # only filtered out ones
for id in trackIDs:
    logger.log(str(id) + ' - ' + str(model.getTrackModel().trackEdges(id)))
#----------------
# Display results
#----------------


sb = SAXBuilder()
document = sb.build( file )
root  = document.getRootElement()
settingsElement = root.getChild( SETTINGS_ELEMENT_KEY )
imageInfoElement = settingsElement.getChild( IMAGE_ELEMENT_KEY );
filename = imageInfoElement.getAttributeValue( IMAGE_FILENAME_ATTRIBUTE_NAME );
folder = imageInfoElement.getAttributeValue( IMAGE_FOLDER_ATTRIBUTE_NAME );
imageFile = File( folder, filename );
dsel = root.getChild(DISPLAY_SETTINGS_ELEMENT_KEY);
imp = IJ.openImage( imageFile.getAbsolutePath() );


#---------------------------------------
# Building a settings object from a file
#---------------------------------------

# Reading the Settings object is actually currently complicated. The
# reader wants to initialize properly everything you saved in the file,
# including the spot, edge, track analyzers, the filters, the detector,
# the tracker, etc...
# It can do that, but you must provide the reader with providers, that
# are able to instantiate the correct TrackMate Java classes from
# the XML data.

# We start by creating an empty settings object
settings = localcreateSettings(imp)

# Then we create all the providers, and point them to the target model:
detectorProvider        = DetectorProvider()
trackerProvider         = TrackerProvider()
spotAnalyzerProvider    = SpotAnalyzerProvider(1)
edgeAnalyzerProvider    = EdgeAnalyzerProvider()
trackAnalyzerProvider   = TrackAnalyzerProvider()
SpotMorphologyAnalyzerProvider =  SpotMorphologyAnalyzerProvider( 1) 



reader.readSettings(imp, detectorProvider, trackerProvider, spotAnalyzerProvider, edgeAnalyzerProvider, trackAnalyzerProvider, SpotMorphologyAnalyzerProvider)


sm = SelectionModel(model)
imp.show();
displayer =  HyperStackDisplayer(model, sm, DisplaySettingsIO.fromJson(dsel.getText()))
displayer.render()
displayer.refresh()






