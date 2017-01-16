# getNLDAS2precipDaily

These two scripts download data from the NLDAS2 forcing dataset at hourly frequency in grib files and get the precipitation data into netcdf files at daily frequency.

The first script to use is a c-shell script. To work it requires setting up an account so you can use wget to download files from NASA, and doing one or two things locally as described here: https://disc.sci.gsfc.nasa.gov/recipes/?q=recipes/How-to-Download-Data-Files-from-HTTP-Service-with-wget

I could not figure out how to do everything in the c-shell, and so the datetime information in the netcdf files it outputs is garbage. But the year and day-of-year are in the filenames.

The second script is a python script that parses the filenames to create the desired datetime info, reading it all into a netcdf-based xarray object, that can easily be written out as a netcdf file. This script does not write out the files, because it is designed to be the first step before doing further analysis in python. 
