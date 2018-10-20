df <- read.csv("pie.csv")
df$category = trimws(df$category)
percent <- function(x, digits = 0, format = "f", ...) {
  paste0(formatC(100 * x, format = format, digits = digits, ...), "%")
}
df_top2 = df[which(df$category == 'Finance, insurance, real estate, rental, and leasing' | df$category == 'Manufacturing'),]

df_other = df[which(df$category != 'Finance, insurance, real estate, rental, and leasing' & df$category != 'Manufacturing'),]
df_top2 
df_top2_temp = df_top2[c("state","percentage","category")]
df_temp = aggregate(percentage ~ state, df_other, sum)
df_temp$category = "Others"

df_new = rbind(df_temp, df_top2_temp)

library(ggplot2)
bp<- ggplot(df_new, aes(x="", y=percentage, fill=category))+
  geom_bar(width = 1, stat = "identity")+ 
  coord_polar("y", start=0)+
  facet_wrap(~state, ncol=5)+
  scale_fill_manual(values=c("green", 'red','deepskyblue'))+
  theme(axis.text.x=element_blank(),legend.position="bottom")+
  geom_text(aes(label = percent(percentage)), position = position_stack(vjust = 0.5))+
  ggtitle("State Economics Pie Chart")+
  theme(plot.title = element_text(hjust = 0.5))

bp