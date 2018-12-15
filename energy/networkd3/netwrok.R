library(networkD3)
edgelist_country <- read.csv('~/Desktop/energy/networkd3/edgelist_country.csv')
nodelist_country <- read.csv('~/Desktop/energy/networkd3/nodelist_country.csv')

forceNetwork(Links = edgelist_country, Nodes = nodelist_country,
             Source = "SourceID", Target = "TargetID",
             Value = "CosSim", NodeID = "NodeName",
             opacity = 0.8,Nodesize='Rate',
             legend = TRUE,Group = "group2",zoom=TRUE,
             colourScale = JS("d3.scaleOrdinal(d3.schemeCategory10);")
             )

