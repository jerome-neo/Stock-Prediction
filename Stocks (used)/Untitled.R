#libraries that we will need
library(FNN)   #knn regression
set.seed(1974) #fix the random generator seed 

#read the data
bmd.data     <- 
  read.csv("aapl.us.txt", 
           stringsAsFactors = TRUE)

#Fit a knn regression with k=3
#using the knn.reg() function from the FNN package
knn3.bmd <- knn.reg(train=bmd.data[c("age")],   
                    y=bmd.data$bmd, 
                    test= data.frame(age=seq(38,89)),
                    k=3)    

plot(bmd.data$age, bmd.data$bmd) #adding the scatter for BMI and BMD
lines(seq(38,89), knn3.bmd$pred)  #adds the knn k=3 line

knn3.bmd.datapred <- knn.reg(train=bmd.data[c("age")],  
                             y=bmd.data$bmd, 
                             test=bmd.data[c("age")], #ORIGINAL DATA
                             k=3)      #knn reg with k=3
#MSE for knn k=3 
mse.knn3  <- mean((knn3.bmd.datapred$pred - bmd.data$bmd)^2)  
mse.knn3

r2.knn3   <- 1- mse.knn3/(var(bmd.data$bmd)*168/169) #R2 for knn k=3 using 
r2.knn3                                              #R2 = 1-MSE/var(y)
