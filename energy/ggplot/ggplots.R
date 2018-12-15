library(ggplot2)
library(gridExtra)

energy <- read.csv('~/Desktop/energy/ggplot/energy.csv')

ggplot(energy, aes(x = crude_oil_production, y = gas_production, size=coal_production)) +
  geom_point(color='blue')+
  ggtitle('Bubble Chart for Relationship Between Crude oil, Nature Gas and Coal Production in 2017')+
  xlab('2017 Crude Oil Production')+
  ylab('2017 Nature Gas Production)')+
  labs(aesthetic='custom text')  

p1 = ggplot(data = energy, aes(x = renew_share, y = energy_intensity)) + 
  geom_point(color='red') +
  geom_smooth(method = "lm", se = FALSE)+
  xlab('Renew Share')+
  ylab('Energy Intensity')+
  ggtitle('Linear Regression between Renew Share Percentage and Energy Intensity')+
  theme(plot.title = element_text(hjust = 0.5))

p2 = ggplot(data = energy, aes(x = co2_intensity, y = energy_intensity)) + 
  geom_point(color='red') +
  geom_smooth(method = "lm", se = FALSE)+
  xlab('CO2 Intensity')+
  ylab('Energy Intensity')+
  ggtitle('Linear Regression between CO2 Intensity Percentage and Energy Intensity')+
  theme(plot.title = element_text(hjust = 0.5))

p3 = ggplot(data = energy, aes(x = co2_intensity, y = renew_share)) + 
  geom_point(color='red') +
  geom_smooth(method = "lm", se = FALSE)+
  xlab('CO2 Intensity')+
  ylab('Renew Share')+
  ggtitle('Linear Regression between CO2 Intensity Percentage and Renew Share Percentage')+
  theme(plot.title = element_text(hjust = 0.5))

grid.arrange(p1, p2, p3,nrow = 2)

'''
ggplot(energy, aes(x="", y=crude_oil_consumption, fill=country))+
  geom_bar(width = 1, stat = "identity")+ 
  coord_polar("y", start=0)+
  facet_wrap(~state, ncol=5)+
  scale_fill_manual(values=c("deepskyblue", "deepskyblue2", "deepskyblue3",'firebrick2','deepskyblue4','forestgreen','dodgerblue','dodgerblue2','dodgerblue3','dodgerblue4','blue'))+
  #theme(axis.text.y = element_text(size=4),
  #strip.text.x = element_text(size=12, color="red",
  #face="bold.italic"),
  #strip.text.y = element_text(size=12, color="red",
  #face="bold.italic"))
  theme(axis.text.x=element_blank())
'''

pie_data <- read.csv('~/Desktop/energy/ggplot/pie_data.csv')

p4 = ggplot(pie_data, aes(x="", y=gas_consumption, fill=country1))+
  geom_bar(width = 1, stat = "identity")+ coord_polar("y", start=0)+
  ggtitle('Pie Graph for Gas Consumption')
  #geom_text(aes(y = gas_consumption/2 + c(0, cumsum(gas_consumption)[-length(gas_consumption)]), label = gas_consumption), size=10)
p4

p5 = ggplot(pie_data, aes(x="", y=crude_oil_consumption, fill=country2))+
  geom_bar(width = 1, stat = "identity")+ coord_polar("y", start=0)+
  ggtitle('Pie Graph for Crude Oil Consumption')

p6 = ggplot(pie_data, aes(x="", y=coal_consumption, fill=country3))+
  geom_bar(width = 1, stat = "identity")+ coord_polar("y", start=0)+
  ggtitle('Pie Graph for Coal Consumption')

grid.arrange(p4, p5, p6,nrow = 2)




