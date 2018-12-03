library(shiny)
library(corrplot)

df_incidence = read.csv('cancer_incidence_state.csv')
df_health = read.csv('health_annual.csv')

df_merge = merge(df_incidence,df_health, by.x = c('AREA','YEAR'),
                 by.y = c('State.Name','Edition'))

# This function will compute correlation score among age adjusted rate, median
# household income, smoking, diabetes and obesity


Income = df_merge[which(df_merge$Measure.Name=='Median Household Income'),]$Value
df_corr = data.frame(Income)
df_corr$Smoking = df_merge[which(df_merge$Measure.Name=='Smoking'),]$Value
df_corr$Diabetes = df_merge[which(df_merge$Measure.Name=='Diabetes'),]$Value
df_corr$Obesity = df_merge[which(df_merge$Measure.Name=='Obesity'),]$Value
df_corr$Income_Inequality = df_merge[which(df_merge$Measure.Name=='Income Inequity'),]$Value
df_corr$Incidence_Rate = df_merge[which(df_merge$Measure.Name=='Income Inequity'),]$AGE_ADJUSTED_RATE


ui <- fluidPage(
  column(12,offset = 5, titlePanel("Correlation Matrix")),
  column(3,
         checkboxGroupInput("icons", "Choose at Least Two Variables:",
                            choiceNames =
                              list('Incidence Rate', 'Income', 'Income Inequality',
                                   'Smoking Rate','Diabetes Rate','Obesity Rate'),
                            choiceValues =
                              list("Incidence_Rate", "Income", "Income_Inequality", "Smoking",
                                   "Diabetes","Obesity"),
                            selected = list("Incidence_Rate", "Income", "Income_Inequality", "Smoking",
                                             "Diabetes","Obesity")
         )
  ),
  
  column(9,
         mainPanel(
           plotOutput('corr_plt',height = 500),
           p(textOutput('caption'))
         )
  )
  
  
)
server <- function(input, output, session) {
  #my_data = df_corr[input$icons]
  #res <- cor(my_data)
  output$caption <- renderText({
    o <- paste(input$icons, collapse = ", ")
    paste("You chose", o)
  })
  output$corr_plt <- renderPlot({
    corrplot(cor(df_corr[input$icons]),method="color",tl.col="black",
             addCoef.col = "black")
  })
  
}

shinyApp(ui, server)

