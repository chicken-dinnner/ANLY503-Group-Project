#package used for map plotting
library(leaflet)
#package used for reading in shape file
library(rgdal)
#read in shape file: https://www.census.gov/geo/maps-data/data/tiger-cart-boundary.html
us.map <- readOGR(dsn = ".", layer = "cb_2017_us_state_20m", stringsAsFactors = FALSE)
us.map = us.map[1:52,]
#us.map$NAME
#a = na.omit(us.map)

df <- read.csv('combine.csv')
df = df[df$NAME != "Puerto Rico", ]
#replace the dataframe in shape.file with the dataframe we created in
#us.map@data = df
us.map = us.map[us.map$NAME != "Puerto Rico", ]
new_df = merge(us.map,df,by = "NAME")

#create a bins palette
mybins_1=c(0,110,120,130,140,150,160,170,180,190,Inf)
mypalette_1 = colorBin( palette="YlGnBu", domain=new_df$AGE_ADJUSTED_RATE_mort, na.color="transparent", bins=mybins_1)

mybins_2=c(0,385,400,420,440,460,480,500,Inf)
mypalette_2 = colorBin( palette="YlOrBr", domain=new_df$AGE_ADJUSTED_RATE_inc, na.color="transparent", bins=mybins_2)

#create a highlight text
mytext=paste("State: ", new_df$NAME,"<br/>", "Age Adjusted Incidence Rate: ", round(new_df$AGE_ADJUSTED_RATE_inc, 2),"<br/>", "Age Adjusted Mortality Rate: ", round(new_df$AGE_ADJUSTED_RATE_mort, 2), sep="") %>%
  lapply(htmltools::HTML)

#create pop up text
population_pop_up <- paste0("<strong>State: </strong>", 
                            new_df$NAME, 
                            "<br><strong>CO2 Rate: </strong>", 
                            new_df$POPULATION)


gmap = leaflet(new_df) %>%
  addTiles()  %>%
  setView( lng=-105, lat=40 , zoom=3) %>%
  #first layer
  addPolygons(
    fillColor = ~mypalette_1(new_df$AGE_ADJUSTED_RATE_mort), stroke=TRUE, fillOpacity = 0.9, color="white", weight=0.3,
    highlight = highlightOptions( weight = 5, color = ~colorNumeric("Blues", new_df$AGE_ADJUSTED_RATE_mort), dashArray = "", fillOpacity = 0.3, bringToFront = TRUE),
    label = mytext,
    labelOptions = labelOptions( style = list("font-weight" = "normal", padding = "3px 8px"), textsize = "13px", direction = "auto"),
    group="Age Adjusted Mortality Rate"
  ) %>%
  #second layer
  addPolygons(
    fillColor = ~mypalette_2(new_df$AGE_ADJUSTED_RATE_inc), stroke=TRUE, fillOpacity = 0.9, color="white", weight=0.3,
    highlight = highlightOptions( weight = 5, color = ~colorNumeric("Blues", new_df$AGE_ADJUSTED_RATE_inc), dashArray = "", fillOpacity = 0.3, bringToFront = TRUE),
    label = mytext,
    labelOptions = labelOptions( style = list("font-weight" = "normal", padding = "3px 8px"), textsize = "13px", direction = "auto"),
    group="Age Adjusted Incidence Rate"
  ) %>%
  
  #marker layer
  addMarkers(data=new_df,lat=new_df$LAT, lng=new_df$LON, popup=population_pop_up, group = "State Info") %>% 
  
  # Layers control
  addLayersControl(
    baseGroups = c("Age Adjusted Mortality Rate"),
    #overlayGroups = c("Rate2","State Info"),
    overlayGroups = c('Age Adjusted Incidence Rate',"State Info"),
    options = layersControlOptions(collapsed = FALSE)
  )

gmap
saveWidget(gmap, 'leaf_let_map.html', selfcontained = TRUE)