library(shiny)
library(ggplot2)

shinyUI(
  fluidPage(
    titlePanel("Boxplots for Energy Data"),
    sidebarLayout(
      sidebarPanel(
        sliderInput("slider1", 
                    label=h3("year"),
                    min=1990, max=2017, value=50, sep="", animate=TRUE),
      hr(),
      helpText("helptext")
    ),
      
      mainPanel(
        plotOutput("boxPlot")
      )
    )
  )
)