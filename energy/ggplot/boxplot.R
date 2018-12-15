library(ggplot2)

#generate dummy data
date_range <- as.Date("2010/06/01") + 0:400
measure <- runif(401)
mydata <- data.frame(date_range, measure)

# create new columns for the months and years, and 
# and a year_month column for x-axis labels
mydata$month <- format(date_range, format="%b")
mydata$year <- as.POSIXlt(date_range)$year + 1900
mydata$year_month <- paste(mydata$year, mydata$month)
mydata$sort_order <- mydata$year *100 + as.POSIXlt(date_range)$mon

#plot it
ggplot(mydata) + geom_boxplot(aes(x=reorder(sort_order, sort_order), y=measure))

df <- read.csv('~/Desktop/ggplot/boxplot.csv')
ggplot(df) + geom_boxplot(aes(x=reorder(year, year), y=renew_share))
