# Plot

forceNetwork(Links = edgelist_state, Nodes = nodelist_state,
             Source = "SourceID", Target = "TargetID",
             Value = "CosSim", NodeID = "NodeName",
             opacity = 0.8,Nodesize='Rate',
             legend = TRUE,Group = "Group",zoom=TRUE,
             colourScale = JS("d3.scaleOrdinal(d3.schemeCategory10);")
             )

