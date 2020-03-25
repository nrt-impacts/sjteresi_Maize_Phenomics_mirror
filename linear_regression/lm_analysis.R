quantiles <- read.csv("quantiles.csv")
View(quantiles)

# Multiple Linear Regression Example
fit <- lm(manual ~ s0.2 + c1.0, data=quantiles)
summary(fit) # show results

# Other useful functions
coefficients(fit) # model coefficients
confint(fit, level=0.95) # CIs for model parameters
fitted_quantiles <- fitted(fit) # predicted values
residual_quantiles <- residuals(fit) # residuals
annova_quantiles <- anova(fit) # anova table
cov_matrix <- vcov(fit) # covariance matrix for model parameters
regression_diagnostics <- influence(fit) # regression diagnostics

# diagnostic plots
layout(matrix(c(1,2,3,4),2,2)) # optional 4 graphs/page
plot(fit)

#MAE calculation
abs_fit <- abs(fit$residuals)
mean(abs_fit)


#look at soil quantile 0.300000 just to check swarm algorithm
fit2 <- lm(manual ~ s0.30000000000000004 + c1.0, data=quantiles)

#compare both via anova
s0.2_s0.3_anova <- anova(fit, fit2)
View(s0.2_s0.3_anova)

# K-fold cross-validation
install.packages("DAAG")
library(DAAG)
str(quantiles)

cv.lm(data=quantiles, fit, m=3) # 3 fold cross-validation


#Exclude point 1305-->scale location plot
quantiles_2 <- quantiles[-c(1305),]
fit_1305 <- lm(manual ~ s0.2 + c1.0, data=quantiles_2)
summary(fit_1305)
layout(matrix(c(1,2,3,4),2,2)) 
plot(fit_1305)

#Exclude multiple outliers
quantiles_4rows <- quantiles[-c(1305, 1420, 28, 1161),]
fit_4rows <- lm(manual ~ s0.2 + c1.0, data=quantiles_4rows)
summary(fit_4rows)
layout(matrix(c(1,2,3,4),2,2)) 
plot(fit_4rows)

#MAE caluclation with removed outliers
abs_fit4rows <- abs(fit_4rows$residuals)
mean(abs_fit4rows)


#Robert's edition of the quantiles with plot name added
finalized_quantiles <- read.csv("quantiles_2.csv")
View(finalized_quantiles)

plot(finalized_quantiles)
library(tidyr)
library(dplyr)
install.packages("reshape2")
library(reshape2)
library(ggplot2)
install.packages("growthcurver")
library(growthcurver)
library(purrr)

#Create new dataframe
regression <- finalized_quantiles %>% select(manual_ht, plot, data_07_02.0.21092202170754804, data_09_02.0.9946622335380833)

#Run linear model to predict hieght
model_new_quantiles <- lm(manual_ht ~ data_07_02.0.21092202170754804 + data_09_02.0.9946622335380833, data=regression)
summary(model_new_quantiles) # show results

#MAE caluclation of new LAS DSM values
abs_new_quantiles <- abs(model_new_quantiles$residuals)
mean(abs_new_quantiles)

# Other useful functions
coefficients(model_new_quantiles) # model coefficients
confint(model_new_quantiles, level=0.95) # CIs for model parameters
fitted_quantiles <- fitted(model_new_quantiles) # predicted values
residual_quantiles <- residuals(model_new_quantiles) # residuals
help(residuals)
View(residual_quantiles)
annova_quantiles <- anova(model_new_quantiles) # anova table
cov_matrix <- vcov(model_new_quantiles) # covariance matrix for model parameters
regression_diagnostics <- influence(model_new_quantiles) # regression diagnostics

#diagnostic plots
layout(matrix(c(1,2,3,4),2,2)) 
plot(model_new_quantiles)

#Exclude multiple outliers
new_quantiles_4rows <- regression[-c(1305, 1420, 28, 1161),]
new_fit_4rows <- lm(manual_ht ~ data_07_02.0.21092202170754804 + data_09_02.0.9946622335380833, data=new_quantiles_4rows)
summary(new_fit_4rows)
layout(matrix(c(1,2,3,4),2,2)) 
plot(new_fit_4rows)

#MAE caluclation with removed outliers
abs_newfit4rows <- abs(new_fit_4rows$residuals)
mean(abs_newfit4rows)





#Introduction to growthcurver
growth_curve <- finalized_quantiles %>% select(plot, data_07_02.0.9946622335380833, data_07_15.0.9946622335380833, data_07_28.0.9946622335380833, data_08_12.0.9946622335380833, data_09_02.0.9946622335380833, data_09_11.0.9946622335380833, data_09_24.0.9946622335380833, data_10_07.0.9946622335380833)
View(growth_curve)
str(growth_curve)

#transposed growth_curve in excel, could not get it to work in R
t_growth_curve <- read.csv("t_growthcurve.csv")
View(t_growth_curve)

names(t_growth_curve)[1] <- "Time"

ggplot(t_growth_curve, aes(x=Time, y=EL19_5098)) + geom_point()

#change row names to times 1-8
time <- c(1,2,3,4,5,6,7,8)
t_growth_curve$time <- time
model.EL19_5098 <- SummarizeGrowth(t_growth_curve$time, t_growth_curve$EL19_5098)
model.EL19_5098$vals
model.EL19_5098
plot(model.EL19_5098)