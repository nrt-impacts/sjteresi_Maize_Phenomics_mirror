# Ruthlessly stolen from:
# https://stats.stackexchange.com/questions/47802/whats-the-most-pain-free-way-to-fit-logistic-growth-curves-in-r

df <- read.csv("../quantiles.csv", header=T)

y <- df$manual_ht
x1 <- df$data_07_02.0.21092202170754804
x2 <- df$data_09_02.0.9946622335380833

htlm <- lm(y ~ x1 + x2)

# subset data
DNase1 <- subset(DNase, Run == 1)

# using a selfStart model
fm1DNase1 <- nls(density ~ SSlogis(log(conc), Asym, xmid, scal), DNase1)
