t_growth_curve2 <- read.csv("t_growthcurve.csv")
library(ggplot2)

View(t_growth_curve2)

names(t_growth_curve2)[1] <- "Time"

ggplot(t_growth_curve2, aes(x=Time, y=EL19_5098)) + geom_point()
View(t_growth_curve)


library(growthcurver)
model.EL19_5098 <- SummarizeGrowth(t_growth_curve2$Time, t_growth_curve2$EL19_5098)
model.EL19_5098$vals
model.EL19_5098
plot(model.EL19_5098)

ggplot(t_growth_curve2, aes(x=Time, y=EL19_6230)) + geom_point()

model.EL19_6230 <- SummarizeGrowth(t_growth_curve2$Time, t_growth_curve2$EL19_6230)
model.EL19_6230$vals
model.EL19_6230
plot(model.EL19_6230)

#EL19_6652
#outlier 1305 aka 6652
ggplot(t_growth_curve2, aes(x=Time, y=EL19_6652)) + geom_point()

model.EL19_6652 <- SummarizeGrowth(t_growth_curve2$Time, t_growth_curve2$EL19_6652)
model.EL19_6652$vals
model.EL19_6652
plot(model.EL19_6652)

#EL19_6768
#outlier 1420
ggplot(t_growth_curve2, aes(x=Time, y=EL19_6768)) + geom_point()

model.EL19_6768 <- SummarizeGrowth(t_growth_curve2$Time, t_growth_curve2$EL19_6768)
model.EL19_6768$vals
model.EL19_6768
plot(model.EL19_6768)

#EL19_6507
#outlier 1161
ggplot(t_growth_curve2, aes(x=Time, y=EL19_6507)) + geom_point()

model.EL19_6507 <- SummarizeGrowth(t_growth_curve2$Time, t_growth_curve2$EL19_6507)
model.EL19_6507$vals
model.EL19_6507
plot(model.EL19_6507)

#EL19_5125
#outlier 28
ggplot(t_growth_curve2, aes(x=Time, y=EL19_5125)) + geom_point()

model.EL19_5125 <- SummarizeGrowth(t_growth_curve2$Time, t_growth_curve2$EL19_5125)
model.EL19_5125$vals
model.EL19_5125
plot(model.EL19_5125)


