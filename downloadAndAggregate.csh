#!/bin/csh
#module load nco

set urlBase = https://hydro1.gesdisc.eosdis.nasa.gov/data/NLDAS/NLDAS_FORA0125_H.002/
set varName = A_PCP_110_SFC_acc
set pre = NLDAS_FORA0125_H
set post = .002

set year = 1982
set sd = 1
set leapYear = 0

while ($year < 2016)
    if ($year % 4 != 0) then #(year is not divisible by 4) 
        set leapYear = 0
    else if ($year % 100 != 0) then #(year is not divisible by 100) then 
        set leapYear = 1
    else if ($year % 400 != 0) then  #(year is not divisible by 400) then 
        set leapYear = 0
    else 
        set leapYear = 1
    endif

    if (leapYear == 1) then
        set ed = 366
    else
        set ed = 365
    endif

    set d = $sd
    while($d < $ed + 1)
        if($d < 10) then
            set threeDigitDay = 00$d
        else if ($d < 100) then
            set threeDigitDay = 0$d       
        else
            set threeDigitDay = $d
        endif

        wget --load-cookies ~/.urs_cookies --save-cookies ~/.urs_cookies --keep-session-cookies -r -c -nH -nd -np -A grb $urlBase$year/$threeDigitDay/
        ncl_convert2nc $pre*$post.grb -v $varName,lat_110,lon_110 -itime -u initial_time3_hours -U time -tps
        ncrcat $pre.A$year*$post.nc $pre.A$year.$d.nc
        cdo daysum $pre.A$year.$d.nc $pre.$year.$threeDigitDay.daysum.nc
        ncatted -O -a forecast_time_units,$varName,o,c,"days" $pre.$year.$threeDigitDay.daysum.nc
        rm -f $pre.*$post.nc
        rm -f $pre.*$post.grb
        rm -f $pre.A$year.$d.nc

        @ d ++
    end #d                                                                                               
    @ year ++
end #y   
