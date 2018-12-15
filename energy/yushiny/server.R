library(shiny)
library(ggplot2)

#energy <- read.csv('~/Desktop/energy/rshiny/box.csv', stringsAsFactors = FALSE)
energy <- read.csv('box.csv', stringsAsFactors = FALSE)

function(input, output) {
  
  output$boxPlot <- renderPlot({
   sub_energy <- energy[which(energy$year==(input$slider1)),]
   tmp <- paste('Year ', input$slider1, sep = " for ")
   ggplot(sub_energy )+
      geom_boxplot(aes(x=type,y=value,fill=type)) +
      ylab('Percentage')+
      theme(axis.text.x = element_text(angle=30,hjust=1)) + 
      ggtitle(tmp)+
      theme(plot.title = element_text(hjust = 0.5, size=18))
    
  }, 
  height = 700)
  
}
