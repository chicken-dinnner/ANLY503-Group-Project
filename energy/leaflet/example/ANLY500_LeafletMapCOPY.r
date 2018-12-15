



##run it after placing all the files in this folder on the desktop 




##HW2 yuyang yy491
## Required datasets are here:
##    CancerCountyFIPS.csv
##    CancerCountyFIPS_Breast.csv
##    LandUseDatasetREALLatlong.csv
##    Data USA - Map of Reimbursements per Medicare Enrollee 
##    Data USA - Map of Poverty Rate by County.csv
##    Data USA - Map of Unemployment by County.csv
## AND ##
############
# Download county shape file.
## !! This is important. Shape files can be found here
#https://www.census.gov/geo/maps-data/data/cbf/cbf_counties.html
#us.map <- tigris::counties(cb = TRUE, year = 2015)
#OR
# Download county shape file from Tiger.
# https://www.census.gov/geo/maps-data/data/cbf/cbf_counties.html
# I downloaded the zip and placed all files in the zip into my RStudio folder
#us.map <- readOGR(dsn = "cb_2016_us_county_20m", layer = "cb_2016_us_county_20m", stringsAsFactors = FALSE)
##head(us.map)
###############
##Not all of these libraries are required for this code, but
## they are good for more generalized goals
############################################################################

library(leaflet)
library(sp)
library(mapproj)
library(maps)
library(mapdata)
library(maptools)
library(htmlwidgets)
library(magrittr)
library(XML)
library(plyr)
library(rgdal)
library(WDI)
library(raster)
library(noncensus)
library(stringr)
library(tidyr)
library(tigris)
library(rgeos)
library(ggplot2)
library(scales)
library(dplyr)

data(zip_codes)
data(counties)

##############################
## REVIEW ALL OF THIS CODE
##############################

##
##Then you will add two layers to it
##
## See the Week 2 Assignment


################################################################
##https://www.statecancerprofiles.cancer.gov/incidencerates/index.php?stateFIPS=99&cancer=001&race=07&sex=
##0&age=001&type=incd&sortVariableName=rate&sortOrder=default#results
CancerRates <- read.csv("CancerCountyFIPS.csv")
#head(CancerRates)
CancerRatesB <- read.csv('CancerCountyFIPS_Breast.csv')
#head(CancerRatesB)
LandUse <- read.csv('LandUseDatasetREALLatlong.csv')
#head(LandUse)
## Not using this dataset yet...
#PowerPlants <- read.csv("PowerPlants.csv")
#head(PowerPlants)

## Make all the column names lowercase
names(CancerRates) <- tolower(names(CancerRates))
#head(CancerRates)

# Rename columns to make for a clean df merge later.
##GEOID is the same as FIPS
colnames(CancerRates) <- c("location", "GEOID", "rate")
#head(CancerRates)
colnames(CancerRatesB) <- c("location", "GEOID", "rate")
#head(CancerRatesB)
colnames(LandUse) <- c("offset", "lat", "lng", "url", "name")
#head(LandUse)

##Add leading zeos to any FIPS code that's less than 5 digits long to get a good match.
##formatC is from C code formatting - creates a 5 digit int
CancerRates$GEOID <- formatC(CancerRates$GEOID, width = 5, format = "d", flag = "0")
#head(CancerRates)
CancerRatesB$GEOID <- formatC(CancerRatesB$GEOID, width = 5, format = "d", flag = "0")
head(CancerRatesB)

## Convert column called location to two columns: State and County
CancerRates <- separate(CancerRates, location, into = c("county", "state"), sep = ", ")
#head(CancerRates)
CancerRatesB <- separate(CancerRatesB, location, into = c("county", "state"), sep = ", ")
#head(CancerRatesB)

##Remove the (...) from the state values
CancerRates[] <- lapply(CancerRates, function(x) gsub("\\s*\\([^\\)]+\\)", "", x))
head(CancerRates)
CancerRatesB[] <- lapply(CancerRatesB, function(x) gsub("\\s*\\([^\\)]+\\)", "", x))
head(CancerRatesB)

##Remove the space# from the end of some of the values in the rate column
CancerRatesB[] <- lapply(CancerRatesB, function(x) gsub("\\#", "", x))
#CancerRatesB

# Convert full state names to abbreviations for a clean df merge later.
CancerRates$state <- state.abb[match(CancerRates$state,state.name)]
#head(CancerRates)
CancerRatesB$state <- state.abb[match(CancerRatesB$state,state.name)]
#head(CancerRatesB)

#Change CancerRates$rate to a number
CancerRates$rate <- as.numeric(as.character(CancerRates$rate))
#head(CancerRates)
CancerRatesB$rate <- as.numeric(as.character(CancerRatesB$rate))
#head(CancerRatesB)


# Download county shape file.
## !! This is important. Shape files can be found here
#https://www.census.gov/geo/maps-data/data/cbf/cbf_counties.html
#us.map <- tigris::counties(cb = TRUE, year = 2015)
#OR
# Download county shape file from Tiger.
# https://www.census.gov/geo/maps-data/data/cbf/cbf_counties.html
# I downloaded the zip and placed all files in the zip into my RStudio folder
us.map <- readOGR(dsn = "cb_2016_us_county_20m", layer = "cb_2016_us_county_20m", stringsAsFactors = FALSE)
head(us.map)
# Remove Alaska(2), Hawaii(15), Puerto Rico (72), Guam (66), Virgin Islands (78), American Samoa (60)
#  Mariana Islands (69), Micronesia (64), Marshall Islands (68), Palau (70), Minor Islands (74)
us.map <- us.map[!us.map$STATEFP %in% c("02", "15", "72", "66", "78", "60", "69",
                                        "64", "68", "70", "74"),]
#head(us.map)

# Make sure other outling islands are removed.
us.map <- us.map[!us.map$STATEFP %in% c("81", "84", "86", "87", "89", "71", "76",
                                        "95", "79"),]

# Merge spatial df with downloaded data.
## This is important
## Now we have our data and the needed carto data
cancermap <- merge(us.map, CancerRates, by=c("GEOID"))
cancermapB <- merge(us.map, CancerRatesB, by=c("GEOID"))

# Format popup data for leaflet map.
popup_dat <- paste0("<strong>County: </strong>", 
                    cancermap$county, 
                    "<br><strong>Cancer Rate (Age Adjusted) Out of 100,000: </strong>", 
                    cancermap$rate)

popup_LU <- paste0("<strong>Use Name: </strong>", 
                   LandUse$name, 
                   "<br><strong>Link: </strong>", 
                   LandUse$url)



############################################################################################

##zip__make zip file easier to merge
zip5<-zip_codes
colnames(zip5)<-c("zip","city","state","lat","lng","GEOID")
zip5$GEOID <- formatC(zip5$GEOID, width = 5, format = "d", flag = "0")

##Reimbursements
##basic data clean
reim<-read.csv("Data USA - Map of Reimbursements per Medicare Enrollee by County.csv")
colnames(reim)<-c("year","county","GEOID","reim_pp")
reim$GEOID<-sub("^.......", "", reim$GEOID)
reim$GEOID <- formatC(reim$GEOID, width = 5, format = "d", flag = "0")
reim <- separate(reim, county, into = c("county", "state"), sep = ", ")
reim[] <- lapply(reim, function(x) gsub("\\#", "", x))
reim$reim_pp <- as.numeric(as.character(reim$reim_pp))
##data select and merge
reim_2014<-filter(reim, year==2014)
reim_2014$state<-NULL
reim2014map <- merge(us.map, reim_2014, by=c("GEOID"))
##print out
write.table(reim2014map,file="cleaned_data_Reimbursements.txt",sep=" ")
##popup data
popup_dat_reim2014 <- paste0("<strong>County Name: </strong>", 
                             reim_2014$county, 
                             "<br><strong>Reimbursements per Medicare Enrollee : </strong>", 
                             reim_2014$reim_pp)

##poverty
##basic data clean and generate
poverty<-read.csv("Data USA - Map of Poverty Rate by County.csv")
##delete the unnecessary
poverty<-poverty[,c(-6:-10)]
##poor population rate
poverty$poverty_rate<-poverty$income_below_poverty/poverty$pop_poverty_status
#color used for marker
poverty$col[poverty$poverty_rate<=0.1] = "yellow"
poverty$col[poverty$poverty_rate>0.1&poverty$poverty_rate<=0.2] = "pink"
poverty$col[poverty$poverty_rate>0.2&poverty$poverty_rate<=0.3] = "red"
poverty$col[poverty$poverty_rate>0.3] = "purple"
colnames(poverty)<-c("year","county","GEOID","poor population","total population","poor_rate","col")
poverty$GEOID<-sub("^.......", "", poverty$GEOID)
poverty$GEOID <- formatC(poverty$GEOID, width = 5, format = "d", flag = "0")
poverty <- separate(poverty, county, into = c("county", "state"), sep = ", ")
poverty[] <- lapply(poverty, function(x) gsub("\\#", "", x))
poverty$poor_rate <- as.numeric(as.character(poverty$poor_rate))
##data selec and merge
poverty_2014<-filter(poverty, year==2014)
poverty_2014$state<-NULL
poverty_2014<-poverty_2014[!duplicated(poverty_2014$GEOID),]
poverty_2014_map0 <- merge(zip5, poverty_2014, by=c("GEOID"))
poverty_2014_map0<-poverty_2014_map0[!duplicated(poverty_2014_map0$GEOID),]
poverty_2014_map0$`total population`<-as.numeric(poverty_2014_map0$`total population`)
##print out
write.table(poverty_2014_map0,file="cleaned_data_poverty.txt",sep=" ")
##data popup
popup_pr <- paste0("<strong>County Name: </strong>", 
                   poverty_2014_map0$city, 
                   "<br><strong>Poor Population Rate:: </strong>", 
                   poverty_2014_map0$poor_rate)

##job
##basic data clean
job<-read.csv("Data USA - Map of Unemployment by County.csv")
job<-job[job$unemployment!="None",]
job$unemployment<-(as.numeric(as.character(job$unemployment)))
##data for marker
job$col[job$unemployment<=0.05] = "green"
job$col[job$unemployment>0.05&job$unemployment<=0.1] = "yellow"
job$col[job$unemployment>0.1] = "red"
job$pop<-paste(job$county,"unempolyment rate: ",job$unemployment_rate)
colnames(job)<-c("year","county","GEOID","unemployment_rate","col","pop")
job$GEOID<-sub("^.......", "", job$GEOID)
job$GEOID <- formatC(job$GEOID, width = 5, format = "d", flag = "0")
job <- separate(job, county, into = c("county", "state"), sep = ", ")
job[] <- lapply(job, function(x) gsub("\\#", "", x))
##data select and merge
job_2015<-filter(job,year==2015)
job_2015$state<-NULL
job_2015_map0<- merge(zip5, job_2015, by=c("GEOID"))
job_2015_map0<-job_2015_map0[!duplicated(job_2015_map0$GEOID),]
##print out
write.table(job_2015_map0,file="cleaned_data_unemployment.txt",sep=" ")
##data popup
popup_dat_job2015 <- paste0("<strong>County Name: </strong>", 
                            job_2015_map0$county, 
                            "<br><strong>unemployment rate: </strong>", 
                            job_2015_map0$unemployment_rate)


#plot part
pal <- colorQuantile("YlOrRd", NULL, n = 9)
pal2 <- colorQuantile("Blues", NULL, n = 9)
## diy icon for unempolyment rate
icon.pop <- awesomeIcons(icon = 'users',
                         markerColor <- job_2015_map0$col,
                         library = 'fa',
                         iconColor = 'black')


gmap <- leaflet(data = cancermap) %>%
  # Base groups
  addTiles() %>%
  setView(lng = -105, lat = 40, zoom = 4) %>% 
  addPolygons(fillColor = ~pal(rate), 
              fillOpacity = 0.8, 
              color = "#BDBDC3", 
              weight = 1,
              popup = popup_dat,
              group="Cancer Rate/100,000 by Counties") %>% 
  
  #Overlay groups
  #Map of Reimbursements per Medicare Enrollee
  addPolygons(data=reim2014map, 
              fillColor = ~pal2(reim_pp), 
              fillOpacity = 0.8, 
              color = "#FFFFCC", 
              weight = 1,
              popup = popup_dat_reim2014,
              group="Map of Reimbursements per Medicare Enrollee") %>% 
  
  addMarkers(data=LandUse,lat=~lat, lng=~lng, popup=popup_LU, group = "Land Use Sites") %>% 
  
  #poor population rate
  addCircleMarkers(color=poverty_2014_map0$col,weight=3,radius=sqrt(as.numeric(poverty_2014_map0$`total population`))/10,clusterOptions = markerClusterOptions(),data=poverty_2014_map0,lat=~lat, lng=~lng, popup=popup_pr, group = "poor population rate") %>% 
  
  #unemployment rate
  addAwesomeMarkers(clusterOptions = markerClusterOptions(),data=job_2015_map0,lng = ~lng, lat = ~lat,label = ~unemployment_rate,icon = icon.pop,group = "unemployment rate") %>% 
  
  #addCircles(~long, ~lat, ~10^mag/5, stroke = F, group = "Quakes") %>%
  #addPolygons(data = outline, lng = ~long, lat = ~lat,
  #           fill = F, weight = 2, color = "#FFFFCC", group = "Outline") %>%
  # Layers control
  addLayersControl(
    baseGroups = c("Cancer Rate/100,000 by Counties"),
    overlayGroups = c("Land Use Sites","Map of Reimbursements per Medicare Enrollee","poor population rate","unemployment rate"),
    options = layersControlOptions(collapsed = FALSE)
  )
gmap
saveWidget(gmap, 'US_county_cancer_poll_map.html', selfcontained = TRUE)