<<<<<<< HEAD
# Ruthlessly stolen from:
# https://stats.stackexchange.com/questions/47802/whats-the-most-pain-free-way-to-fit-logistic-growth-curves-in-r

library("nls")

# subset data
DNase1 <- subset(DNase, Run == 1)

# using a selfStart model
fm1DNase1 <- nls(density ~ SSlogis(log(conc), Asym, xmid, scal), DNase1)
=======
# Ruthlessly stolen from:
# https://stats.stackexchange.com/questions/47802/whats-the-most-pain-free-way-to-fit-logistic-growth-curves-in-r

library("nls")

# subset data
DNase1 <- subset(DNase, Run == 1)

# using a selfStart model
fm1DNase1 <- nls(density ~ SSlogis(log(conc), Asym, xmid, scal), DNase1)
>>>>>>> 458063e80116965c7a0c8e0ef958bd3b2d8ba35e
