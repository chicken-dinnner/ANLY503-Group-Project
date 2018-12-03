library(shiny)
library(corrplot)
library(dplyr)
library(ggplot2)
library(rsconnect)
rsconnect::setAccountInfo(name='yanchenwang', token='D5D46BEF6CF5B60C18847B3D3A050424', secret='K84WHeoXCNNh5NUbvEfNQe7oEK8qL29PMgO83QT+')

rate <- read.csv('cancer_incidence_state.csv')
rate$cancer_rate = rate$AGE_ADJUSTED_RATE
mort <- read.csv('cancer_mortality_state.csv')
mort$cancer_rate = mort$AGE_ADJUSTED_RATE
df = rbind(rate,mort)

ui <- fluidPage(
  
  column(12,offset = 3, titlePanel("Incidence and Mortality Rate by States")),
  column(12,offset = 3,
         sidebarPanel(
           radioButtons('choice','Choose either Incidence Rate or Mortality Rate',
                        choiceNames = list('Incidence Rate','Mortality Rate'),
                        choiceValues = list('Incidence','Mortality')),
           width = 5
         )
  ),
  column(6,
         sidebarPanel(
           checkboxGroupInput("t_state", "Choose from Five States with Highest Cancer Rate:",
                              choiceNames =
                                list('Arkansas','Kenturcky','Louisiana','Mississippi','West Virginia'),
                              choiceValues =
                                list("Arkansas", "Kenturcky", "Louisiana", "Mississippi",
                                     "West Virginia"),
                              selected = list("Louisiana")),
           width = 10
         )
  ),
  column(6,
         sidebarPanel(
           checkboxGroupInput("l_state", "Choose from Five States with Lowest Cancer Rate:",
                              choiceNames =
                                list('Arizona','California','Colorado','New Mexico','Utah'),
                              choiceValues =
                                list("Arizona", "California", "Colorado", "New Mexico",
                                     "Utah"),
                              selected = list("California")),
           width = 10
         )
  ),
  
  mainPanel(
    plotOutput('line_chart',height = "500px",width = "800px")
  )
  
  
  
)
server <- function(input, output, session) {
  selectData = reactive({
    temp = df[df$AREA %in% c(input$t_state,input$l_state),]
    temp = temp[temp$EVENT_TYPE %in% input$choice,]
    #temp1 =df[df$AREA %in% input$l_state,]
    #my_data = rbind(temp,temp1)
    return(temp)
  })
  towrite = reactive({
    a = paste(paste("Line Chart of Cancer", input$choice),"Rate")
    return(a)})
  #temp1 = df[df$AREA %in% input$l_state,]
  #my_data = selectData()
  output$line_chart <- renderPlot({
    ggplot(data=selectData(), 
           aes(x=YEAR, y=cancer_rate,col=AREA))+
      geom_line()+
      theme(plot.title = element_text(size=22,hjust = 0.5))+
      ggtitle(towrite())
    
  },height = 600, width = 1000)
  
  
  
}

shinyApp(ui, server)

