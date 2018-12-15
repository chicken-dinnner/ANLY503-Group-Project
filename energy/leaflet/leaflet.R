library(leaflet)
# Download .shp file on the web:
download.file("http://thematicmapping.org/downloads/TM_WORLD_BORDERS_SIMPL-0.3.zip" , destfile="world_shape_file.zip")
system("unzip world_shape_file.zip")

# Read the file with the rgdal library in R
library(rgdal)
world_spdf=readOGR( dsn= getwd() , layer="TM_WORLD_BORDERS_SIMPL-0.3")
# Look at the info provided with the geospatial object
#head(world_spdf@data)
#summary(world_spdf@data)

df <- read.csv('~/Desktop/energy/leaflet/combine.csv')
#world_spdf@data = merge(x = world_spdf@data, y = energy, by = "NAME", all.x = TRUE)
world_spdf@data = df

# Modify these info
world_spdf@data$POP2005[ which(world_spdf@data$POP2005 == 0)] = NA
world_spdf@data$POP2005 = as.numeric(as.character(world_spdf@data$POP2005)) / 1000000 %>% round(2)


# Create a color palette with handmade bins.
mybins_o=c(-360,-260,-160,-60,0,60,160,260,360,Inf)
mypalette_o = colorBin( palette="YlGnBu", domain=world_spdf@data$crude_oil_balance, na.color="transparent", bins=mybins_o)

mybins_g=c(-360,-260,-160,-60,0,60,160,260,360,Inf)
mypalette_g = colorBin( palette="YlOrBr", domain=world_spdf@data$gas_balance, na.color="transparent", bins=mybins_g)

mybins_c=c(-380,-260,-160,-60,0,60,160,260,360,Inf)
mypalette_c = colorBin( palette="Greens", domain=world_spdf@data$coal_balance, na.color="transparent", bins=mybins_c)

# Prepar the text for the tooltip:
mytext_o=paste("Country: ", world_spdf@data$NAME,"<br/>", "Area: ", world_spdf@data$AREA, "<br/>", "Crude Oil Trade Balance: ", round(world_spdf@data$crude_oil_balance, 2), sep="") %>%
  lapply(htmltools::HTML)

mytext_g=paste("Country: ", world_spdf@data$NAME,"<br/>", "Area: ", world_spdf@data$AREA, "<br/>", "Natural Gas Trade Balance: ", round(world_spdf@data$gas_balance, 2), sep="") %>%
  lapply(htmltools::HTML)

mytext_c=paste("Country: ", world_spdf@data$NAME,"<br/>", "Area: ", world_spdf@data$AREA, "<br/>", "Coal Trade Balance: ", round(world_spdf@data$coal_balance, 2), sep="") %>%
  lapply(htmltools::HTML)

co2_text <- paste0("<strong>Country: </strong>", 
                   df$NAME, 
                   "<br><strong>CO2 Intensity: </strong>", 
                   df$co2_intensity)



    
gmap <- leaflet(data = world_spdf) %>%
  # Base groups
  addTiles() %>%
  setView(lat=10, lng=0 , zoom=2) %>% 
  addPolygons(fillColor = ~mypalette_o(df$crude_oil_balance), stroke=TRUE, fillOpacity = 0.9, color="white", weight=0.3,
              highlight = highlightOptions( weight = 5, color = ~colorNumeric("Blues", df$crude_oil_balance)(df$crude_oil_balance), dashArray = "", fillOpacity = 0.3, bringToFront = TRUE),
              label = mytext_o,
              labelOptions = labelOptions( style = list("font-weight" = "normal", padding = "3px 8px"), textsize = "13px", direction = "auto"),
              group="Crude Oil Trade Balance") %>% 
  
  #Overlay groups
  #Map of Reimbursements per Medicare Enrollee
  addPolygons(fillColor = ~mypalette_g(df$gas_balance), stroke=TRUE, fillOpacity = 0.9, color="white", weight=0.3,
              highlight = highlightOptions( weight = 5, color = ~colorNumeric("Blues", df$gas_balance)(df$gas_balance), dashArray = "", fillOpacity = 0.3, bringToFront = TRUE),
              label = mytext_g,
              labelOptions = labelOptions( style = list("font-weight" = "normal", padding = "3px 8px"), textsize = "13px", direction = "auto"),
              group="Natural Gas Trade Balance") %>% 
  
  addPolygons(fillColor = ~mypalette_c(df$coal_balance), stroke=TRUE, fillOpacity = 0.9, color="white", weight=0.3,
              highlight = highlightOptions( weight = 5, color = ~colorNumeric("Blues", df$coal_balance)(df$coal_balance), dashArray = "", fillOpacity = 0.3, bringToFront = TRUE),
              label = mytext_c,
              labelOptions = labelOptions( style = list("font-weight" = "normal", padding = "3px 8px"), textsize = "13px", direction = "auto"),
              group="Coal Trade Balance") %>% 
  

  addMarkers(data=df,lat=df$LAT, lng=df$LON, popup=co2_text, group = "CO2 Intensity") %>% 
  
  # Layers control
  addLayersControl(
    baseGroups = c("Crude Oil Trade Balance"),
    overlayGroups = c("Natural Gas Trade Balance","Coal Trade Balance","CO2 Intensity"),
    options = layersControlOptions(collapsed = FALSE)
  )


gmap    

    
    


  
    
    
    
    
    
    
    
    
    
    
    