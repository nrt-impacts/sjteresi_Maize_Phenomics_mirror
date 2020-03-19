# Ruthlessly stolen from:
# https://stats.stackexchange.com/questions/47802/whats-the-most-pain-free-way-to-fit-logistic-growth-curves-in-r

library("nls")

# subset data
DNase1 <- subset(DNase, Run == 1)

# using a selfStart model
fm1DNase1 <- nls(density ~ SSlogis(log(conc), Asym, xmid, scal), DNase1)
