library(ggplot2)
library(dplyr)

eco <- read.csv("pie.csv")
rate <- read.csv('~/Desktop/cancer_incidence_state.csv')

df1 <- eco
df2 <- rate[rate$AREA %in% c('Utah','Colorado','New Mexico','Arizona','California','Arkansas','Louisiana','West Virginia','Mississippi','Kentucky'),]

# Basic line plot with points
ggplot(data=df2, aes(x=YEAR, y=AGE_ADJUSTED_RATE, group=AREA)) +
  geom_line(color="blue", size=1.2)+
  geom_point(color="red", size=3)+
  facet_wrap(~AREA, ncol=4)+
  theme(axis.text.y = element_text(size=4),
        strip.text.x = element_text(size=12, color="red",
                                    face="bold.italic"),
        strip.text.y = element_text(size=12, color="red",
                                    face="bold.italic"))+
  ggtitle('                                                                       line Chart for Cancer Incidence by State in USA from 1999 to 2015')




