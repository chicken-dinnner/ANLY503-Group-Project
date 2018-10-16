library(ggplot2)
library(gridExtra)
ca <- read.csv("ca.csv")
ak <- read.csv("ak.csv")

p1<-ggplot(ca, aes(x = year, y = rate, size=Manufacturing)) +
  geom_point(color='blue')+
  ggtitle('Manufacturing Bubble Graph for California')
p2<-ggplot(ca, aes(x = year, y = rate, size=Finance_Real_Estate)) +
  geom_point(color='blue')+
  ggtitle('Finance_Real_Estate Bubble Graph for California')

p3<-ggplot(ak, aes(x = year, y = rate, size=Manufacturing)) +
  geom_point()+
  ggtitle('Manufacturing Bubble Graph for Arkansas')
p4<-ggplot(ak, aes(x = year, y = rate, size=Finance_Real_Estate)) +
  geom_point()+
  ggtitle('Finance_Real_Estate Bubble Graph for Arkansas')

grid.arrange(p1, p2, p3, p4, nrow = 2)
