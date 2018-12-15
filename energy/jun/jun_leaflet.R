library(leaflet)
# Download .shp file on the web:
#download.file("http://thematicmapping.org/downloads/TM_WORLD_BORDERS_SIMPL-0.3.zip" , destfile="world_shape_file.zip")
#system("unzip world_shape_file.zip")

# Read the file with the rgdal library in R
library(rgdal)
world_spdf=readOGR( dsn= getwd() , layer="TM_WORLD_BORDERS_SIMPL-0.3")
# Look at the info provided with the geospatial object
#head(world_spdf@data)
#summary(world_spdf@data)

df <- read.csv('~/Desktop/leafletdata.csv')
world_spdf@data = df

# Modify these info
world_spdf@data$POP2005[ which(world_spdf@data$POP2005 == 0)] = NA
world_spdf@data$POP2005 = as.numeric(as.character(world_spdf@data$POP2005)) / 1000000 %>% round(2)


# Create a color palette with handmade bins.
mybins=c(0,1000000,10000000,30000000,70000000,100000000,300000000,600000000,Inf)
mypalette_pop = colorBin( palette="YlGnBu", domain=world_spdf@data$Population, na.color="transparent", bins=mybins)

# Prepar the text for the tooltip:
#mytext_cc=paste("Country: ", world_spdf@data$NAME,"<br/>", "Area: ", world_spdf@data$AREA, "<br/>", "Coal Consumption: ", round(world_spdf@data$coal_consumption, 2), sep="") %>%
  #lapply(htmltools::HTML)

biocap_text <- paste0("<strong>Country: </strong>", 
                   df$NAME, 
                   "<br><strong>Total.BiocapTotGHA: </strong>", 
                   df$Total.BiocapTotGHA)

ef_text <- paste0("<strong>Country: </strong>", 
                      df$NAME, 
                      "<br><strong>Total.EFConsTotGHA: </strong>", 
                      df$Total.EFConsTotGHA)

icon.pop <- awesomeIcons(icon = 'users',
                         markerColor <- df$Total.EFConsTotGHA,
                         library = 'fa',
                         iconColor = 'black')



gmap <- leaflet(data = world_spdf) %>%
  # Base groups
  addTiles() %>%
  setView(lat=10, lng=0 , zoom=2) %>% 
  addPolygons(fillColor = ~mypalette_pop(df$Population), stroke=TRUE, fillOpacity = 0.9, color="white", weight=0.3,
              #highlight = highlightOptions( weight = 5, color = ~colorNumeric("Blues", df$coal_production)(df$coal_production), dashArray = "", fillOpacity = 0.3, bringToFront = TRUE),
              #label = mytext_cp,
              #labelOptions = labelOptions( style = list("font-weight" = "normal", padding = "3px 8px"), textsize = "13px", direction = "auto"),
              group="2014 Population") %>% 
  
  #Overlay groups
  
  addMarkers(data=df,lat=df$LAT, lng=df$LON, popup=biocap_text, group = "Biocapacity") %>% 
  
  #addMarkers(data=df,lat=df$LAT, lng=df$LON, popup=ef_text, group = "ef_text", icon = leafIcons) %>% 
  
  addAwesomeMarkers(clusterOptions = markerClusterOptions(),data=df,lat=df$LAT, lng=df$LON, popup=ef_text,label = df$Total.EFConsTotGHA,icon = icon.pop,group = "Ecological Consumption") %>% 
  
  # Layers control
  addLayersControl(
    baseGroups = c("2014 Population"),
    overlayGroups = c("Biocapacity","Ecological Consumption"),
    options = layersControlOptions(collapsed = FALSE)
  )


gmap    

    

    
    
    
    
    
    
    
    
    
    