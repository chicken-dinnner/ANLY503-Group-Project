library(ggplot2)
df <- read.csv("regression.csv")
# create multiple linear model
lm_fit_diabetes <- lm(r ~ d, data=df)
summary(lm_fit_diabetes)
lm_fit_smoking <- lm(r ~ s, data=df)
summary(lm_fit_smoking)


# save predictions of the model in the new data frame 
# together with variable you want to plot against
#predicted_df <- data.frame(mpg_pred = predict(lm_fit, df), d=df$d)

# this is predicted line comparing only chosen variables
ggplot(data = df, aes(x = d, y = r)) + 
  geom_point(color='red') +
  geom_smooth(method = "lm", se = FALSE)+
  xlab('Diabetes People per 100 People')+
  ylab('Cancer People per 10K People')+
  ggtitle('Linear Regression between Cancer Incidence Rate and Diabetes Rate')+
  theme(plot.title = element_text(hjust = 0.5))



# this is predicted line comparing only chosen variables
ggplot(data = df, aes(x = s, y = r)) + 
  geom_point(color='red') +
  geom_smooth(method = "lm", se = FALSE)+
  xlab('Smoking People per 100 People')+
  ylab('Cancer People per 100K People')+
  ggtitle('Linear Regression between Cancer Incidence Rate and Smoking Rate')+
  theme(plot.title = element_text(hjust = 0.5))
