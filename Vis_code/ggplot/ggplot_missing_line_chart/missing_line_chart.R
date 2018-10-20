cancer_incidence_state <- read.csv("cancer_incidence_state.csv")
df <- cancer_incidence_state[cancer_incidence_state$AREA %in% c('Arkansas','Mississippi','South Dakota','Alabama'),]

library(ggplot2)
# Basic line plot with points
ggplot(data=df, aes(x=YEAR, y=AGE_ADJUSTED_RATE, group=AREA)) +
  geom_line(color="blue", size=1.2)+
  geom_point(color="red", size=3)+
  facet_wrap(~AREA, ncol=4)+
  theme(axis.text.y = element_text(size=4),
        strip.text.x = element_text(size=12, color="red",
                                    face="bold.italic"),
        strip.text.y = element_text(size=12, color="red",
                                    face="bold.italic"))+
  ggtitle('                                          line Chart for Cancer Incidence by State in USA from 1999 to 2015')+
  xlab('Year')+
  ylab('Age Adjusted Cancer Rate (Number per 100K People)')
