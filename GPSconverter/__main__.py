import pkg_resources
import gpxpy
import pandas as pd
import numpy as np
import os
import re
import shutil
import folium
import PIL.Image
from PIL import ImageTk, ImageEnhance
from tkinter import PhotoImage, Toplevel
from tkinter import Canvas
from tkinter import Tk
from tkinter import END
from tkinter import INSERT
from tkinter import Label
from tkinter import Button
from tkinter import filedialog
from tkinter import messagebox
from tkinter import scrolledtext
from html2image import Html2Image 
import json
import simplekml
from tkmacosx import Button

import geopandas as gpd
import fiona 
import shapefile

# import array
# import matplotlib.pyplot as plt

# conda install cartopy...
# import cartopy                                  
# import cartopy.crs as ccrs                      
# import cartopy.io.img_tiles as cimgt

def main(args=None):

    
    window = Tk()

    image = pkg_resources.resource_filename('GPSconverter', 'DATA/LOGO.gif')
    photo = PhotoImage(file=image)
    w = photo.width()
    h = photo.height()
    cv = Canvas(window, width=w, height=h)
    cv.create_image(0,0, image=photo, anchor='nw')
    cv.grid(column=0, row=0) 

    window.title("GPSconverer BY CARMELO SAMMARCO")

    #########################
    #Functions 
    #########################

    def selfile():
        selfile.input_file = filedialog.askopenfilename()


    def selfolder():
        selfolder.Home_dir = filedialog.askdirectory()

    def getData():
        GPSfile=selfile.input_file
        data = open(GPSfile).read()
        text = str(data)
        txt.insert(INSERT,text)

    def cleanData():
        txt.delete(1.0,END)
    
    def exportdata():
        file = selfolder.Home_dir + "/Export.txt"
        f = open(file, 'w')
        f.write(txt.get('1.0', 'end'))
        f.close()
        messagebox.showinfo('FYI', 'File Saved.')
    
    def toCSV():
        GPSfile=selfile.input_file
        data = open(GPSfile).read()
        fileout = selfolder.Home_dir + "/Output.csv"
        lat =  np.array(re.findall(r'lat="([^"]+)',data),dtype=float)
        lon =  np.array(re.findall(r'lon="([^"]+)',data),dtype=float)
        ele = np.array(re.findall(r'<ele>([^\<]+)',data),dtype=float)
        time = re.findall(r'<time>([^\<]+)',data)
        if  len(ele)==0 and len(time)==0 and len(lat)>0 and len(lon)>0:
            combined = np.array(list(zip(lat,lon)))
            df = pd.DataFrame(combined, columns = ['Latitude','Longitude'])
            df.to_csv(fileout, index=False)
        
        elif len(ele)>0 and len(time)==0 and len(lat)>0 and len(lon)>0:
            combined = np.array(list(zip(lat,lon,ele)))
            df = pd.DataFrame(combined, columns = ['Latitude','Longitude','Elevation'])
            df.to_csv(fileout, index=False)

        elif len(ele)==0 and len(time)>0 and len(lat)>0 and len(lon)>0:
            combined = np.array(list(zip(lat,lon,time)))
            df = pd.DataFrame(combined, columns = ['Latitude','Longitude','Time'])
            df.to_csv(fileout, index=False)

        else:
            combined = np.array(list(zip(lat,lon,ele,time)))
            df = pd.DataFrame(combined, columns = ['Latitude','Longitude','Elevation','Time'])
            df.to_csv(fileout, index=False)
    

        
    def toJSON():
        GPSfile=selfile.input_file
        data = open(GPSfile).read()
        fileout = selfolder.Home_dir + "/Output.json"

        lat =  np.array(re.findall(r'lat="([^"]+)',data),dtype=float)
        lon =  np.array(re.findall(r'lon="([^"]+)',data),dtype=float)
        ele = np.array(re.findall(r'<ele>([^\<]+)',data),dtype=float)
        time = re.findall(r'<time>([^\<]+)',data)
        
        if  len(ele)==0 and len(time)==0 and len(lat)>0 and len(lon)>0:
            combined = np.array(list(zip(lat,lon)))
            df = pd.DataFrame(combined, columns = ['Latitude','Longitude'])
            df.to_json(fileout)
        
        elif len(ele)>0 and len(time)==0 and len(lat)>0 and len(lon)>0:
            combined = np.array(list(zip(lat,lon,ele)))
            df = pd.DataFrame(combined, columns = ['Latitude','Longitude','Elevation'])
            df.to_json(fileout)

        elif len(ele)==0 and len(time)>0 and len(lat)>0 and len(lon)>0:
            combined = np.array(list(zip(lat,lon,time)))
            df = pd.DataFrame(combined, columns = ['Latitude','Longitude','Time'])
            df.to_json(fileout)

        else:
            combined = np.array(list(zip(lat,lon,ele,time)))
            df = pd.DataFrame(combined, columns = ['Latitude','Longitude','Elevation','Time'])
            df.to_json(fileout)


    def toGEOJSONpoint():
        toCSV()
        filein = selfolder.Home_dir + "/Output.csv"
        data_frame = pd.read_csv(filein,infer_datetime_format=True,na_values=[''])
        json_result_string = data_frame.to_json(orient='records', double_precision=12,date_format='iso')
        json_result = json.loads(json_result_string)
        geojson = {
            'type': 'FeatureCollection',
            'features': []
        }
        for record in json_result:
            geojson['features'].append({
                'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': [record['Longitude'], record['Latitude']],
                },
                'properties': record,
            })
        with open(selfolder.Home_dir + "/Points.geojson", 'w') as f:
            f.write(json.dumps(geojson, indent=2))
        os.remove(selfolder.Home_dir + "/Output.csv")
    

    def toGEOJASONtrack():
        toCSV()
        filein = selfolder.Home_dir + "/Output.csv"
        data_frame = pd.read_csv(filein,infer_datetime_format=True,na_values=[''])
        json_result_string = data_frame.to_json(orient='records', double_precision=12,date_format='iso')
        json_result = json.loads(json_result_string)
        geojson = {
            'type': 'FeatureCollection',
            'features': []
        }
        listcoor = []
        for record in json_result:
            listcoor.append([record['Longitude'], record['Latitude']])
        geojson['features'].append({
            'type': 'Feature',
            'geometry': {
                'type': 'LineString',
                'coordinates': listcoor,
            },
            'properties': record,
        })
        with open(selfolder.Home_dir + "/Track.geojson", 'w') as f:
            f.write(json.dumps(geojson, indent=4))
        os.remove(selfolder.Home_dir + "/Output.csv")

    
    def toshp_point():
        toGEOJSONpoint()
        infile = selfolder.Home_dir + "/Points.geojson"
        gdf = gpd.read_file(infile)
        gdf.to_file(selfolder.Home_dir + "/Points.shp")
        os.remove(selfolder.Home_dir + "/Points.geojson")
    

    def toshp_line():
        toGEOJASONtrack()
        infile = selfolder.Home_dir + "/Track.geojson"
        gdf = gpd.read_file(infile)
        gdf.to_file(selfolder.Home_dir + "/Track.shp")
        os.remove(selfolder.Home_dir + "/Track.geojson")

    
    def toKmz():
        toCSV()
        filein = selfolder.Home_dir + "/Output.csv"
        data_frame = pd.read_csv(filein,infer_datetime_format=True,na_values=[''])
        json_result_string = data_frame.to_json(orient='records', double_precision=12,date_format='iso')
        json_result = json.loads(json_result_string)
        listcoor = []
        for record in json_result:
            listcoor.append([record['Longitude'], record['Latitude']])
        kml = simplekml.Kml()
        ls = kml.newlinestring(name='A LineString')
        ls.coords = listcoor
        ls.extrude = 1
        ls.altitudemode = simplekml.AltitudeMode.relativetoground
        ls.style.linestyle.width = 5
        ls.style.linestyle.color = simplekml.Color.blue
        kml.save(selfolder.Home_dir +'/Output.kml')
        kml.save(selfolder.Home_dir +'/Output.kmz')
        os.remove(selfolder.Home_dir + "/Output.csv")

    

    def generate_html():
        GPSfile=selfile.input_file
        gpx = gpxpy.parse(open(GPSfile)) 
        #(1)make DataFrame
        track = gpx.tracks[0]
        segment = track.segments[0]
        # Load the data into a Pandas dataframe (by way of a list)
        data = []
        #segment_length = segment.length_3d()
        for point_idx, point in enumerate(segment.points):
            data.append([point.longitude, point.latitude,point.elevation,point.time, segment.get_speed(point_idx)])
            columns = ['Longitude', 'Latitude', 'Altitude', 'Time', 'Speed']
            df = pd.DataFrame(data, columns=columns)
        #2(make points tuple for line)
        points = []
        for track in gpx.tracks:
            for segment in track.segments: 
                for point in segment.points:
                    points.append(tuple([point.latitude, point.longitude]))   
        mappa = folium.Map(location=[df.Latitude.mean(), df.Longitude.mean()], tiles=None, zoom_start=10, control_scale=True, control=True)
        track = folium.PolyLine(points, color="blue", weight=5, popup="Track")
        track.add_to(mappa)
        folium.TileLayer('openstreetmap', name='OpenStreetMap').add_to(mappa)
        folium.TileLayer('stamenterrain', name='Terrain').add_to(mappa)
        folium.TileLayer('Stamen Toner', name='Black&White').add_to(mappa)
        folium.LayerControl().add_to(mappa)
        mappa.add_child(folium.LatLngPopup())
        mappa.save(selfolder.Home_dir + "/index.html", 'w')
    


    def htmltoim():
        generate_html()
        hti = Html2Image()
        hti.output_path = selfolder.Home_dir 
        hti.screenshot(html_file= selfolder.Home_dir + "/index.html",save_as="MAP.png")
        load = PIL.Image.open(selfolder.Home_dir + "/MAP.png")
        enhancer = ImageEnhance.Contrast(load)
        factor = 10 #increase contrast
        im_output = enhancer.enhance(factor)
        im_output.save(selfolder.Home_dir + "/MAP.png")
        

    # def tomap():
    #     # Open and parse your GPX file.
    #     trackFile = selfile.input_file
    #     track = gpxpy.parse(open(trackFile))
    #     # Make an iterator over the points in the GPS track.
    #     trackPoints = track.walk()
    #     # Make empty arrays to put the latitudes an longitudes in.
    #     lats = array.array('f')
    #     lons = array.array('f')
    #     # Iterate over all points an populate the latitude and longitude arrays.
    #     for p in trackPoints:
    #         lats.append(float(p[0].latitude))
    #         lons.append(float(p[0].longitude))
    #     # Get the minimum and maximum latitudes and longitudes from the GPS track.
    #     bounds = track.get_bounds()
    #     request = cimgt.StamenTerrain()
    #     fig = plt.figure(figsize=(10,10), dpi=300, tight_layout=True)
    #     ax = plt.axes(projection=request.crs)
    #     #ax = plt.axes(projection=ccrs.PlateCarree())
    #     plt.title('MAP OVERVIEW')
    #     zoom = 14
    #     ax.add_image(request, zoom)
    #     plt.plot(lons, lats, 'm-', transform=ccrs.PlateCarree(), linewidth=3)
    #     plt.savefig(selfolder.Home_dir + "/MAP.png")


        
    def previewfrohtmlim():
        generate_html()
        htmltoim()
        imfix = PIL.Image.open(selfolder.Home_dir + "/MAP.png")
        #resize = imfix.resize((w, h), PIL.Image.LANCZOS)
        resize = imfix.resize((int(imfix.size[0]/2),int(imfix.size[1]/2)), 0)
        render = ImageTk.PhotoImage(resize)
        windowpop = Toplevel(window)
        img = Label(windowpop, image=render)
        img.image = render
        img.grid(column=0, row=0)
        os.remove(selfolder.Home_dir + "/index.html")



    # def previewfrommap():
    #     #generate_html()
    #     #htmltoim()
    #     tomap()
    #     imfix = PIL.Image.open(selfolder.Home_dir + "/MAP.png")
    #     #resize = imfix.resize((w, h), PIL.Image.LANCZOS)
    #     resize = imfix.resize((int(imfix.size[0]/2),int(imfix.size[1]/2)), 0)
    #     render = ImageTk.PhotoImage(resize)
    #     windowpop = Toplevel(window)
    #     img = Label(windowpop, image=render)
    #     img.image = render
    #     img.grid(column=0, row=0)
        
    

    def publish_map():
        source = selfolder.Home_dir + "/index.html"
        target = selfolder.Home_dir + "/WebAPP/templates/"
        os.makedirs(target)
        shutil.copy(source, target)
        f = open(selfolder.Home_dir + "/WebAPP/FlaskApp.py",'w')
        script= """
from flask import Flask, render_template
import webbrowser

app = Flask(__name__)
@app.route('/')
def webmap():
    return render_template("index.html")
if __name__ == '__main__':
    webbrowser.open_new('http://127.0.0.1:5000/')
    app.run()"""
        f.write(script)
        f.close()   
        os.chdir(selfolder.Home_dir + "/WebAPP/")
        os.system("python FlaskApp.py")


    #######################
    #GUI interface 
    #######################

    btn = Button(window, text="SELECT DATA", bg="green2", command=selfile)
    btn.grid(column=0, row=1)
    ###
    ###
    btn = Button(window, text="OUTPUT FOLDER", bg="green2", command=selfolder)
    btn.grid(column=0, row=2)
    ###
    space = Label(window, text="")
    space.grid(column=0, row=3)
    ###
    btn = Button(window, text="VIEW DATA", bg="yellow", command=getData)
    btn.grid(column=0, row=4)
    ###
    txt = scrolledtext.ScrolledText(window,width=68,height=20)
    txt.grid(column=0,row=5)
    ###
    btn = Button(window, text="EXPORT DATA", bg="yellow", command=exportdata)
    btn.grid(column=0, row=6)
    ###
    btn = Button(window, text="CLEAR DATA VIEW", bg="yellow", command=cleanData)
    btn.grid(column=0, row=7)
    ###
    space = Label(window, text="")
    space.grid(column=0, row=8)
    ###
    btn = Button(window, text="PREVIEW MAP", bg="deep sky blue", command=previewfrohtmlim)  
    btn.grid(column=0, row=9)
    ###
    space = Label(window, text="")
    space.grid(column=0, row=10)
    ####
    btn = Button(window, text="TO CSV", bg="orange", command=toCSV) 
    btn.grid(column=0, row=11)
    ###
    btn = Button(window, text="TO KML/KMZ", bg="orange", command=toKmz) 
    btn.grid(column=0, row=12)
    ###
    btn = Button(window, text="TO JSON", bg="orange", command=toJSON) 
    btn.grid(column=0, row=13)
    ##
    btn = Button(window, text="TO HTML", bg="orange", command=generate_html) 
    btn.grid(column=0, row=14)
    ##
    btn = Button(window, text="TO RASTER", bg="orange", command=htmltoim)  
    btn.grid(column=0, row=15)
    ##
    btn = Button(window, text="TO GEOJSON (POINTS)", bg="orange", command=toGEOJSONpoint) 
    btn.grid(column=0, row=16)
    ##
    btn = Button(window, text="TO GEOJSON (LINE)", bg="orange", command=toGEOJASONtrack) 
    btn.grid(column=0, row=17)
    ##
    btn = Button(window, text="TO SHAPE-FILE (POINTS)", bg="orange", command=toshp_point) 
    btn.grid(column=0, row=18)
    ##
    btn = Button(window, text="TO SHAPE-FILE (LINE)", bg="orange", command=toshp_line) 
    btn.grid(column=0, row=19)
    ##
    btn = Button(window, text=" TO FLASK PROJECT", bg="orange", command=publish_map)  
    btn.grid(column=0, row=20)

    #################################################################

    window.mainloop()