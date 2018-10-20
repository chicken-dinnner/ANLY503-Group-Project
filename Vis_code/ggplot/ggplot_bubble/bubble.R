library(ggplot2)
library(gridExtra)
ca <- read.csv("ca.csv")
ak <- read.csv("ak.csv")

p1<-ggplot(ca, aes(x = year, y = rate, size=Manufacturing)) +
  geom_point(color='blue')+
  ggtitle('Bubble Chart for Gross Output Value (K) for Manufacturing Industry in California')+
  xlab('Year')+
  ylab('Cancer Incidence Rate (Number per 100K People)')+
  labs(aesthetic='custom text')     
p2<-ggplot(ca, aes(x = year, y = rate, size=Finance_Real_Estate)) +
  geom_point(color='blue')+
  ggtitle('Bubble Chart for Gross Output Value (K) for Finance Real Estate in California')+
  xlab('Year')+
  ylab('Cancer Incidence Rate (Number per 100K People)')+
  scale_fill_continuous("Town Name",guide = guide_legend())
p3<-ggplot(ak, aes(x = year, y = rate, size=Manufacturing)) +
  geom_point()+
  ggtitle('Bubble Chart for Gross Output Value (K) for Manufacturing Industry in Arkansas')+
  xlab('Year')+
  ylab('Cancer Incidence Rate (Number per 100K People)')
  #opts(group="Town Name")
p4<-ggplot(ak, aes(x = year, y = rate, size=Finance_Real_Estate)) +
  geom_point()+
  ggtitle('Bubble Chart for Gross Output Value (K) for Finance Real Estate in Arkansas')+
  xlab('Year')+
  ylab('Cancer Incidence Rate (Number per 100K People)')

grid.arrange(p1, p2, p3, p4, nrow = 2)

