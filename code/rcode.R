library(fitdistrplus)
df <- read.table('C:\\Users\\D\\Desktop\\拟合分布实验（2只股票，示例）.csv',head=T,sep=",") # input file
codes <- unique(df$code)
code <- c()
shape <- c()
scale <- c()
for (i in codes){
  data <- df[which(df$code==i),]
  fw <- fitdist(data$recp_ri, "weibull")
  es <- fw$estimate
  code <- c(code,i)
  shape <- c(shape,es['shape'])
  scale <- c(scale,es['scale'])
}
out_put <- data.frame(code=code,shape=shape,scale=scale)
write.csv(out_put, file = "c://Users//D//Desktop//result.csv", row.names = F, quote = F) # output file