# Plot
library(networkD3)
edgelist_state = read.csv('edgelist_state.csv')
nodelist_state = read.csv('nodelist_state.csv')
forceNetwork(Links = edgelist_state, Nodes = nodelist_state,
             Source = "SourceID", Target = "TargetID",
             Value = "CosSim", NodeID = "NodeName",
             opacity = 0.8,Nodesize='Rate',
             legend = TRUE,Group = "Group",zoom=TRUE,
             colourScale = JS("d3.scaleOrdinal(d3.schemeCategory10);")
)

