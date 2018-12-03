
library(plotly)
df <- read.csv("regression.csv")
# create multiple linear model
fit <- lm(r ~ d+s, data=df)
summary(fit)

# predict over sensible grid of values

grid <- with(df, expand.grid(seq(min(df$d)-5,max(df$d)+7,0.3), seq(min(df$s)-5,max(df$s)+7,0.3)))
df1 <- setNames(data.frame(grid), c("d", "s"))
vals <- predict(fit, newdata = df1)

# form matrix and give to plotly
m <- matrix(vals, nrow = length(seq(min(df$d)-5,max(df$d)+7,0.3)), ncol = length(seq(min(df$s)-5,max(df$s)+7,0.3)))

mysample <- df[sample(1:nrow(df), 300,
                          replace=FALSE),]

p <- plot_ly(x = mysample$d, y = mysample$s, z = mysample$r,name='Data Point') %>%
  add_markers()%>%
  layout(title='Multiple Regression between Cancer Incidence Rate and Smoking Rate, Diabetes Rate',
         scene = list(xaxis = list(title = 'Diabetes Rate'),
                      yaxis = list(title = 'Smoking Rate'),
                      zaxis = list(title = 'Cancer Incidence Rate')))
p = p %>% add_surface(x = seq(min(df$d)-5,max(df$d)+7,0.3), y = seq(min(df$s)-5,max(df$s)+7,0.3), z = m,name='Regression Plane')
p

chart_link = api_create(p, filename="3d_rotatable")
chart_link





