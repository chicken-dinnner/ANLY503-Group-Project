library(ggplot2)
library(plotly)
library(gridExtra)

df <- read.csv('~/Desktop/energy/plotly/energy.csv')

data <- df[, c('country', 'gas_production')]

#colors <- c('rgb(211,94,96)', 'rgb(128,133,133)', 'rgb(144,103,167)', 'rgb(171,104,87)', 'rgb(114,147,203)')
colors <- c('rgb(211,94,96)','rgb(114,147,203)')

p1 <- plot_ly(data, labels = ~country, values = ~gas_production, type = 'pie',
             textposition = 'inside',
             textinfo = 'label+percent',
             insidetextfont = list(color = '#FFFFFF'),
             hoverinfo = 'text',
             text = ~paste('$', gas_production, ' bcm'),
             marker = list(colors = colors,
                           line = list(color = '#FFFFFF', width = 1)),
             #The 'pull' attribute can also be used to create space between the sectors
             showlegend = FALSE) %>%
  #add_pie(domain = list(x = c(0.25, 0.75), y = c(0, 0.6))) %>%
  layout(title = 'Global Nature Gas Production (bcm)',
         xaxis = list(showgrid = FALSE, zeroline = FALSE, showticklabels = FALSE),
         yaxis = list(showgrid = FALSE, zeroline = FALSE, showticklabels = FALSE))

p2 <- plot_ly(df, labels = ~country, values = ~crude_oil_production, #type = 'pie',
             textposition = 'inside',
             textinfo = 'label+percent',
             insidetextfont = list(color = '#FFFFFF'),
             hoverinfo = 'text',
             text = ~paste('$', crude_oil_production, ' Mt'),
             marker = list(colors = colors,
                           line = list(color = '#FFFFFF', width = 1)),
             #The 'pull' attribute can also be used to create space between the sectors
             showlegend = FALSE) %>%
  add_pie(pull=0.2) %>%
  layout(title = 'Global Crude Oil Production (Mt)',
         xaxis = list(showgrid = FALSE, zeroline = FALSE, showticklabels = FALSE),
         yaxis = list(showgrid = FALSE, zeroline = FALSE, showticklabels = FALSE))

p3 <- plot_ly(df, labels = ~country, values = ~coal_production, #type = 'pie',
              textposition = 'inside',
              textinfo = 'label+percent',
              insidetextfont = list(color = '#FFFFFF'),
              hoverinfo = 'text',
              text = ~paste('$', gas_production, ' Mt'),
              marker = list(colors = colors,
                            line = list(color = '#FFFFFF', width = 1)),
              #The 'pull' attribute can also be used to create space between the sectors
              showlegend = FALSE) %>%
  add_pie(hole=0.2, pull=0.2) %>%
  layout(title = 'Global Coal Production (Mt)',
         xaxis = list(showgrid = FALSE, zeroline = FALSE, showticklabels = FALSE),
         yaxis = list(showgrid = FALSE, zeroline = FALSE, showticklabels = FALSE))

Sys.setenv("plotly_username"="yu2theyang")
Sys.setenv("plotly_api_key"="GTKHfBQGfz9oChgwUYny")
chart_link1 <- api_create(p2,filename = 'Global Nature Gas Production (Mt)')
chart_link1
chart_link2 <- api_create(p2,filename = 'Global Crude Oil Production (Mt)')
chart_link2
chart_link3 <- api_create(p2,filename = 'Global Coal Production (Mt)')
chart_link3