
# Import arcpy module
import arcpy, os, glob
from arcpy import env
 
# Script arguments
InHUCS = arcpy.GetParameterAsText(0)
if InHUCS == '#' or not InHUCS:
    InHUCS = "KS_wbdhuc12_a" # provide a default value if unspecified
 
ExportLocation = arcpy.GetParameterAsText(1)
if ExportLocation == '#' or not ExportLocation:
    ExportLocation = "D:\\TWIP\\Batch_Env" # provide a default value if unspecified
 
BufferDistance = arcpy.GetParameterAsText(2)
if BufferDistance == '#' or not BufferDistance:
    BufferDistance = "100 Meters" # provide a default value if unspecified
 
SelectedHucs = "Selected_hucs.shp"
SelectedHucsBuffer = "Selected_hucs_Buffer.shp"
 
HucsForBuffer = os.path.join(ExportLocation, SelectedHucs)
SelectedHucsBuffer = os.path.join(ExportLocation, SelectedHucsBuffer)
 
arcpy.env.workspace = ExportLocation
 
# Process: Feature Class to Feature Class, Buffer, Split
arcpy.FeatureClassToFeatureClass_conversion(InHUCS, ExportLocation, SelectedHucs, "", "", "")
arcpy.Buffer_analysis(HucsForBuffer, SelectedHucsBuffer, BufferDistance, "FULL", "ROUND", "NONE", "")
arcpy.Split_analysis(SelectedHucsBuffer, SelectedHucsBuffer, "HUC_12", ExportLocation, "")
 
# Cleans up Selected_hucs.shp and Selected_hucs_Buffer.shp if they exist
for filename in [SelectedHucs, SelectedHucsBuffer]:
    if arcpy.Exists(filename):
        arcpy.Delete_management(filename)
    arcpy.AddMessage('%s deleted' % filename)

#Puts all shapefile names into a list. Takes off .shp extension.
shapefiles = glob.glob(os.path.join(ExportLocation, '*.shp'))
boundaries = [w.replace('.shp', '') for w in shapefiles]
 
#Creates directories from the list.
for boundary in boundaries:
    if not os.path.exists(boundary):
        os.mkdir(boundary)
    arcpy.AddMessage('Directory made for ' + boundary)
