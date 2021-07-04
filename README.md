# GPSconverter (Global-Positioning-System Converter)

[![Build Status](https://travis-ci.com/carmelosammarco/GPSconverter.png)](https://travis-ci.com/carmelosammarco/GPSconverter)[![PyPi](https://img.shields.io/badge/PyPi-Project-yellow.svg)](https://pypi.org/project/GPSconverter/)

![Imgur](https://i.imgur.com/jbCBPkh.png)


 The idea to developed this **Python based application for manipulating/view GPS data** borned while I was doing some trekking because I wanted a fast way to convert all the file saved and plot them automatically. As many development and during the process I added many other features :) Hope you like it! 

It can be usefull when:

- You want to visualise your GPS raw data, modified them and export as txt file

- You want have a fast preview of your GPS data on a map which can be done with a render of the folium HTML web page or using the powerfull Generic Mapping Tool (GMT). The creation of a Flask project is also possible.

- You need to convert GPS data to other formats (for example the tracks/waypoints of your outdoor activity) for further processing/scopes you could have.

- You want to visualize your data using the native Google Earth engine extention (KML/KMZ)

- You want to generate an HTML file ready for be embedded in your website or published into a server. 

and many more.... 

**Inside the project folder (GPSconverter)/DATA you can find a "test_data" folder with inside a GPX file so to be able to use the application and verify that all work well.**

## Installation

The best way is create an ad-hoc environment with the anaconda python distribution and more specifically throught the "yml" file using the following command:

```
conda env create -f name-environment.yml
```

You can download the "yml' file needed (in the above example as name-environment.yml) clicking the badge here below: 

[![Anaconda-Server Badge](https://anaconda.org/csammarco/gpsx/badges/installer/env.svg)](https://anaconda.org/CSammarco/gpsx)

The command to run the process in your machine and using the file previously downloaded is:

```
conda env create -f GPSX.yml
```

then to activate the environmet:

```
conda activate GPSX
```

Once you installed the anaconda environment you should be able to have all the packages needed instaled (The GPSconverter Application too!). 

If for some reason you want to install it using just pypi repository (be aware that in this case you need to install GMT manually and for that you can find more info [here](https://github.com/GenericMappingTools/gmt/blob/master/INSTALL.md#cross-platform-install-instructions)). The command to install this tool using Pypi is the following:

```
pip install GPSconverter
```

Anyway, once you decice how to proceed (by conda environment or Pypi repository) to run the application just type on your terminal/command_propt the following:

```
GPSconverter
```

At this point a GUI interface will pop up and you are ready to go! Below what you are going to see for different OS:

<p align="center">
  <img width="" height="380" src="PIC/GUIs.png">
</p>


## Conversions avaiable

- **Convert from GPX to CSV**

- **Convert from GPX to KML/KMZ**

- **Convert from GPX to JSON**

- **Convert from GPX to HTML**

- **Convert from GPX to RASTER**

- **Convert from GPX to GeoJSON(Points)**

- **Convert from GPX to GeoJSON(Line)**

- **Convert from GPX to Shapefile(Line)**

- **Convert from GPX to Shapefile(Line)**

I have still ideas and improvements that can be done ( it is an infinite process and it will never stop for me) but anyway it is a good base to start with... Feel free to "fork" and contribute!


## Stand alone version:

At the moment it is a working in progress. The aim is to be able to realise an executable to run without any python requirements/installation and natively for both Window and MacOS operative systems. However, it is still a working in progress and just application icon is ready.. here below:

![Imgur](https://i.imgur.com/1zIm0KGs.png)

Enjoy :)
