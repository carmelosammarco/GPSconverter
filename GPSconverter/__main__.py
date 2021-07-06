from tkinter.constants import TRUE
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
from tkinter import ttk
from tkinter import END
from tkinter import INSERT
from tkinter import Label
from tkinter import Button
from tkinter import filedialog
from tkinter import messagebox
from tkinter import scrolledtext
from html2image import Html2Image 
import json
import csv
import simplekml
from tkmacosx import Button
import geopandas as gpd
import pygmt



def main(args=None):

    window = Tk()

    image = pkg_resources.resource_filename('GPSconverter', 'DATA/LOGO.gif')
    photo = PhotoImage(file=image)
    w = photo.width()
    h = photo.height()
    cv = Canvas(window, width=w, height=h)
    cv.create_image(0,0, image=photo, anchor='nw')
    #cv.grid(column=0, row=0) 
    cv.pack(side='top')

    tab_control = ttk.Notebook(window)
    tab1 = ttk.Frame(tab_control)
    tab2 = ttk.Frame(tab_control)
    tab3 = ttk.Frame(tab_control)
    tab4 = ttk.Frame(tab_control)
    tab_control.add(tab1, text='INPUT')
    tab_control.add(tab2, text='CSV-CONVERTER')
    tab_control.add(tab3, text='GPX-CONVERTER')
    tab_control.add(tab4, text='MAPS')

    window.title("GPSconverer BY CARMELO SAMMARCO")


    #########################
    #Functions 
    #########################

    def selfile():
        selfile.input_file = filedialog.askopenfilename()

    def selfolder():
        selfolder.Home_dir = filedialog.askdirectory()

    def viewinput():
        global txt
        windowpop = Toplevel(tab1)
        txt = scrolledtext.ScrolledText(windowpop,width=100,height=50)
        txt.pack()
        GPSfile=selfile.input_file
        data = open(GPSfile).read()
        text = str(data)
        txt.insert(INSERT,text)
        btn = Button(windowpop, text="EXPORT AS .TXT FILE", bg="yellow", command=exportdata)
        btn.pack()
    
    def exportdata():
        file = selfolder.Home_dir + "/Export.txt"
        f = open(file, 'w')
        f.write(txt.get('1.0', 'end'))
        f.close()
        messagebox.showinfo('FYI', 'File Saved.')
    
    def CSVtoGPX():
        CSV = selfile.input_file
        df = pd.read_csv(CSV) 
        Latitude = [] #0
        Longitude = [] #1
        Elevation = [] #2
        Time = [] #3	
        for n in range(0,len(CSV)):
            with open(CSV,encoding='utf-8',mode='r') as csvfile: #closes file automatically with completion of block
                csvdata = csv.reader(csvfile, delimiter=',')		        
        for index, row in df.iterrows():
            Latitude.append(row[0])
            Longitude.append(row[1])
            Elevation.append(row[2])
            Time.append(row[3])
        with open(selfolder.Home_dir + "/Output.gpx", encoding='utf-8', mode='w') as of:	
            #header
            of.write('<?xml version="1.0" encoding="utf-8" standalone="yes"?>')
            of.write("\n")
            of.write('<gpx version="1.1" creator="GPSconverter https://github.com/carmelosammarco/GPSconverter">') 
            of.write("\n")
            of.write("<trk>")
            of.write("\n")
            of.write("  <name>Output</name>")
            of.write("\n")
            of.write("  <trkseg>")
            of.write("\n")
            #write trackpoints here
            for i in range(0, len(Latitude)):
                # #lat,lon
                of.write("    <trkpt lat=\"")
                of.write('%.15f' % Latitude[i])
                of.write("\" lon=\"")
                of.write('%.15f' % Longitude[i])
                of.write("\">\n")
                #Elevation
                if(Elevation[i]):
                    of.write("      <ele>")
                    of.write(str(Elevation[i]))
                    of.write("</ele>\n")
                else:
                    of.write("      <ele>")
                    of.write(str(0))
                    of.write("</ele>\n")
                #time
                if(len(Time[i])>0):
                    of.write("      <time>")
                    of.write(Time[i])
                    of.write("</time>\n")
                    #of.write("\n")
                    of.write("    </trkpt>")
                    of.write("\n")    
            #end of file
            of.write("  </trkseg>")
            of.write("\n")
            of.write("</trk>")
            of.write("\n")
            of.write("</gpx>")

    def GPXtoCSV():
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

    def GPXtoJSON():
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

    def GPXtoGEOJSONpoint():
        GPXtoCSV()
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
    
    def GPXtoGEOJASONtrack():
        GPXtoCSV()
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
  
    def GPXtoshp_point():
        GPXtoGEOJSONpoint()
        infile = selfolder.Home_dir + "/Points.geojson"
        gdf = gpd.read_file(infile)
        gdf.to_file(selfolder.Home_dir + "/Points.shp")
        os.remove(selfolder.Home_dir + "/Points.geojson")
    
    def GPXtoshp_line():
        GPXtoGEOJASONtrack()
        infile = selfolder.Home_dir + "/Track.geojson"
        gdf = gpd.read_file(infile)
        gdf.to_file(selfolder.Home_dir + "/Track.shp")
        os.remove(selfolder.Home_dir + "/Track.geojson")
   
    def GPXtoKmz():
        GPXtoCSV()
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
        mappa = folium.Map(location=[df.Latitude.mean(), df.Longitude.mean()], tiles=None, zoom_start=12, control_scale=True, control=True)
        track = folium.PolyLine(points, color="blue", weight=5, popup="Track")
        track.add_to(mappa)
        folium.TileLayer('openstreetmap', name='OpenStreetMap').add_to(mappa)
        folium.TileLayer('stamenterrain', name='Terrain').add_to(mappa)
        folium.TileLayer('Stamen Toner', name='Black&White').add_to(mappa)
        folium.LayerControl().add_to(mappa)
        mappa.add_child(folium.LatLngPopup())
        mappa.save(selfolder.Home_dir + "/index.html", 'w')
    
    def htmlrender():
        generate_html()
        hti = Html2Image()
        hti.output_path = selfolder.Home_dir 
        hti.screenshot(html_file= selfolder.Home_dir + "/index.html",save_as="MAP.png")
        load = PIL.Image.open(selfolder.Home_dir + "/MAP.png")
        enhancer = ImageEnhance.Contrast(load)
        factor = 10 #increase contrast
        im_output = enhancer.enhance(factor)
        im_output.save(selfolder.Home_dir + "/MAP.png")
   
    def previewfromhtml():
        generate_html()
        htmlrender()
        imfix = PIL.Image.open(selfolder.Home_dir + "/MAP.png")
        #resize = imfix.resize((w, h), PIL.Image.LANCZOS)
        resize = imfix.resize((int(imfix.size[0]/2),int(imfix.size[1]/2)), 0)
        render = ImageTk.PhotoImage(resize)
        windowpop = Toplevel(window)
        img = Label(windowpop, image=render)
        img.image = render
        img.grid(column=0, row=0)
        os.remove(selfolder.Home_dir + "/index.html")
        
    def CSVtoGMTmap():
        CSVfile = selfile.input_file
        lats = []
        lons = []
        df = pd.read_csv(CSVfile, infer_datetime_format=True, na_values=['']) 
        for index, row in df.iterrows():
             lats.append(row[0])
             lons.append(row[1])
        zoommapregion_scale = 2
        zoominsregion_scale = 20
        region =[ 
            df.Longitude.min() -zoommapregion_scale,
            df.Longitude.max() +zoommapregion_scale,
            df.Latitude.min() -(zoommapregion_scale/2),
            df.Latitude.max() +(zoommapregion_scale/2), ]
        regionins=[
            df.Longitude.min() -zoominsregion_scale,
            df.Longitude.max() +zoominsregion_scale, 
            df.Latitude.min()  -(zoominsregion_scale/2),
            df.Latitude.max()  +(zoominsregion_scale/2), ]
        #pointxmean = df.Longitude.mean()
        #pointymean = df.Latitude.mean() 
        rectangle = [[region[0], region[2], region[1], region[3]]]
        #pygmt.config(MAP_FRAME_TYPE="plain")
        pygmt.config(FORMAT_GEO_MAP="ddd.xx")
        #define topo data file and CPTs
        topo_data = '@earth_relief_30s' 
        #topo_data = 'add a local one in app... ??'
        #CPTtopo = ' add a local one in app... ??'
        CPTtopo = 'dem4'   
        proj = "M20c"
        fig = pygmt.Figure()
        pygmt.grdcut(grid=topo_data, outgrid=selfolder.Home_dir  + '/topo.grd', region=region)
        pygmt.grd2cpt(grid=selfolder.Home_dir + '/topo.grd', region=region, cmap=CPTtopo, continuous=True) 
        fig.basemap(region=region, projection=proj, frame=[ "a", "+tGPX-MAP"])
        fig.grdimage( 
            grid=selfolder.Home_dir  + '/topo.grd', 
            cmap=CPTtopo,
            region=region,
            projection=proj,
            shading=True,
            frame='a'
            )
        fig.coast(
            region=region,
            projection=proj,
            water='skyblue',
            resolution='f',
            shorelines=True,
            lakes=True,
            rivers='a',
            frame='a'
        )
        fig.grdcontour(
            #annotation=500,
            interval=200,
            grid=topo_data,
            limit=[0, 5000],
            projection=proj,
            frame='a'
        )
        fig.plot(
            x=lons,
            y=lats,
            pen="1p,red",
        ) 
        #fig.plot(x=pointx, y=pointy, style="c1c", color="red", pen="black", frame='a')
        fig.colorbar(
            frame=['a', "x+lElevation"]
        )
        ################################################
        with fig.inset(position="jBL+w4.6c/3c+o0.2c/0.2c", box="+gwhite+p2p"):
            #pygmt.config(MAP_FRAME_TYPE="plain")
            # Use a plotting function to create a figure inside the inset
            rectangle = [[region[0], region[2], region[1], region[3]]]
            fig.coast(
                region=regionins,
                projection="M?",
                land="grey",
                borders=[1, 2],
                shorelines="1/thin",
                water="blue",   
            )
            fig.plot(data=rectangle, style="r+s", pen="0.4p,red")
        ###############################################
        fig.savefig(selfolder.Home_dir + "/MAPgmtfromCSV.png",  transparent=False, crop=True, anti_alias=True, dpi=300)

    def viewGMTcsv():
        CSVtoGMTmap()
        imfix = PIL.Image.open(selfolder.Home_dir + "/MAPgmtfromCSV.png")
        #resize = imfix.resize((w, h), PIL.Image.LANCZOS)
        resize = imfix.resize((int(imfix.size[0]/2),int(imfix.size[1]/2)), 0)
        render = ImageTk.PhotoImage(resize)
        windowpop = Toplevel(window)
        img = Label(windowpop, image=render)
        img.image = render
        img.grid(column=0, row=0)

    def GPXtoGMTmap():
        GPSfile= selfile.input_file
        gpx = gpxpy.parse(open(GPSfile)) 
        track = gpx.tracks[0]
        segment = track.segments[0]
        data = []
        lats = []
        lons = []
        for point_idx, point in enumerate(segment.points):
            data.append([point.longitude, point.latitude, point.elevation, point.time, segment.get_speed(point_idx)])
            lats.append(point.latitude)
            lons.append(point.longitude)
            columns = ['Longitude', 'Latitude', 'Altitude', 'Time', 'Speed']
            df = pd.DataFrame(data, columns=columns)
        zoommapregion_scale = 2
        zoominsregion_scale = 20
        region =[ 
            df.Longitude.min() -zoommapregion_scale,
            df.Longitude.max() +zoommapregion_scale,
            df.Latitude.min() -(zoommapregion_scale/2),
            df.Latitude.max() +(zoommapregion_scale/2), ]
        regionins=[
            df.Longitude.min() -zoominsregion_scale,
            df.Longitude.max() +zoominsregion_scale, 
            df.Latitude.min()  -(zoominsregion_scale/2),
            df.Latitude.max()  +(zoominsregion_scale/2), ]
        #pointxmean = df.Longitude.mean()
        #pointymean = df.Latitude.mean() 
        rectangle = [[region[0], region[2], region[1], region[3]]]
        #pygmt.config(MAP_FRAME_TYPE="plain")
        pygmt.config(FORMAT_GEO_MAP="ddd.xx")
        #define topo data file and CPTs
        topo_data = '@earth_relief_30s' 
        #topo_data = 'add a local one in app... ??'
        #CPTtopo = ' add a local one in app... ??'
        CPTtopo = 'dem4'   
        proj = "M20c"
        fig = pygmt.Figure()
        pygmt.grdcut(grid=topo_data, outgrid=selfolder.Home_dir  + '/topo.grd', region=region)
        pygmt.grd2cpt(grid=selfolder.Home_dir + '/topo.grd', region=region, cmap=CPTtopo, continuous=True) 
        fig.basemap(region=region, projection=proj, frame=[ "a", "+tGPX-MAP"])
        fig.grdimage( 
            grid=selfolder.Home_dir  + '/topo.grd', 
            cmap=CPTtopo,
            region=region,
            projection=proj,
            shading=True,
            frame='a'
            )
        fig.coast(
            region=region,
            projection=proj,
            water='skyblue',
            resolution='f',
            shorelines=True,
            lakes=True,
            rivers='a',
            frame='a'
        )
        fig.grdcontour(
            #annotation=500,
            interval=200,
            grid=topo_data,
            limit=[0, 5000],
            projection=proj,
            frame='a'
        )
        fig.plot(
            x=lons,
            y=lats,
            pen="1p,red",
        ) 
        #fig.plot(x=pointx, y=pointy, style="c1c", color="red", pen="black", frame='a')
        fig.colorbar(
            frame=['a', "x+lElevation"]
        )
        ################################################
        with fig.inset(position="jBL+w4.6c/3c+o0.2c/0.2c", box="+gwhite+p2p"):
            #pygmt.config(MAP_FRAME_TYPE="plain")
            # Use a plotting function to create a figure inside the inset
            rectangle = [[region[0], region[2], region[1], region[3]]]
            fig.coast(
                region=regionins,
                projection="M?",
                land="grey",
                borders=[1, 2],
                shorelines="1/thin",
                water="blue",   
            )
            fig.plot(data=rectangle, style="r+s", pen="0.4p,red")
        ###############################################
        fig.savefig(selfolder.Home_dir + "/MAPgmtfromGPX.png",  transparent=False, crop=True, anti_alias=True, dpi=300)

    def viewGMTgpx():
        GPXtoGMTmap()
        imfix = PIL.Image.open(selfolder.Home_dir + "/MAPgmtfromGPX.png")
        #resize = imfix.resize((w, h), PIL.Image.LANCZOS)
        resize = imfix.resize((int(imfix.size[0]/2),int(imfix.size[1]/2)), 0)
        render = ImageTk.PhotoImage(resize)
        windowpop = Toplevel(window)
        img = Label(windowpop, image=render)
        img.image = render
        img.grid(column=0, row=0)
        
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

    ###TAB 1
    space = Label(tab1, text="")
    space.pack()
    ###TAB 1
    btn = Button(tab1, text="SELECT FILE", bg="red", command=selfile)
    btn.pack()
    ###
    btn = Button(tab1, text="OUTPUT FOLDER", bg="red", command=selfolder)
    btn.pack()
    ###
    space = Label(tab1, text="")
    space.pack()
    ###
    btn = Button(tab1, text="VIEW DATA", bg="yellow", command=viewinput)
    btn.pack()
    ###

    ### TAB 2
    space = Label(tab2, text="")
    space.pack()
    ###
    btn = Button(tab2, text="CSV TO GPX", bg="green2", command=CSVtoGPX) 
    btn.pack()


    ###TAB 3
    space = Label(tab3, text="")
    space.pack()
    ####
    btn = Button(tab3, text="GPX TO CSV", bg="orange", command=GPXtoCSV) 
    btn.pack()
    ###
    btn = Button(tab3, text="GPX TO JSON", bg="orange", command=GPXtoJSON) 
    btn.pack()
    ##
    btn = Button(tab3, text="GPX TO HTML", bg="orange", command=generate_html) 
    btn.pack()
    ##
    btn = Button(tab3, text="GPX TO KML/KMZ", bg="orange", command=GPXtoKmz) 
    btn.pack()
    ##
    btn = Button(tab3, text="GPX TO GEOJSON (LINE)", bg="orange", command=GPXtoGEOJASONtrack) 
    btn.pack()
    ##
    btn = Button(tab3, text="GPX TO SHAPE-FILE (LINE)", bg="orange", command=GPXtoshp_line) 
    btn.pack()
    ##
    btn = Button(tab3, text="GPX TO GEOJSON (POINTS)", bg="orange", command=GPXtoGEOJSONpoint) 
    btn.pack()
    ##
    btn = Button(tab3, text="GPX TO SHAPE-FILE (POINTS)", bg="orange", command=GPXtoshp_point) 
    btn.pack()
    ##





    ###TAB 4
    space = Label(tab4, text="")
    space.pack()
    ###
    btn = Button(tab4, text="GPX TO MAP", bg="deep sky blue", command=viewGMTgpx)  
    btn.pack()
    ###
    btn = Button(tab4, text="CSV TO MAP", bg="deep sky blue", command=viewGMTcsv)  
    btn.pack()
    ###
    btn = Button(tab4, text="HTML-RENDER", bg="deep sky blue", command=previewfromhtml)  
    btn.pack()
    ###
    btn = Button(tab4, text="FLASK PROJECT", bg="deep sky blue", command=publish_map)  
    btn.pack()
    ###

    #################################################################

    tab_control.pack(expand=1, fill='both')

    window.mainloop()