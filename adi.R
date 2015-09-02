library(readr)
library(foreach)
library(doParallel)
library(caret)
library(caTools)

#read in the data set
a <- read_delim("F:\\ISS\\Semester 2\\Assignments\\Data Analytics\\vd.csv", col_names=TRUE, delim=';')

a <- data.frame(a)

# ensure the target binomial variables are factors for classification
a$visit <- factor(a$visit)
a$conversion <- factor(a$conversion)


# Phase 1 - Visit classificaion
# remove Cust. ID, conversion and spend
b <- a[,-c(1,12,13)]

# select people who visited and who did not visit separately
vis <- b[which(b$visit==1),]
notf <- not <- b[which(b$visit!=1),]


# create parallel processing environment for 2 (TWO) processors
#cl<-makeCluster(2)
#registerDoParallel(cl)

iter <- 6
predTable <- modelsCoef <- predic <- NULL
modelsCoef <- rep(0,10)
modelsCoef <- data.frame(modelsCoef)

#k=f=
for (i in 1:5){
  # randomly select training & testing set from Visited customers
  pos <- sample(nrow(vis),size=floor(nrow(vis)/10*7),replace=FALSE)
  train<- vis[pos,]
  test<- vis[-pos,]
  
  # create distinct and non-repeatable bags for Non-visited customers
  sel <- sample(nrow(not), size=9246, replace=FALSE)
  #train1 <-1:nrow(not) %in% sel
  no <- not[sel,]
  not <- not[-sel,]
  
  # randomly select training & testing set from Non-Visited customers
  pos1 <- sample(nrow(no),size=floor((nrow(no)/10)*7),replace=FALSE)
  trainNo <- no[pos1,]
  testNo <- no[-pos1,]
  
  # combine the train & test Bags of both Visit & Non-Visit customers
  trainSet <- rbind(train,trainNo)
  testSet <- rbind(test,testNo)
  
  # logistic regression model build
  fit <- glm(visit~., data=trainSet, family=binomial)
  h <- data.frame(cbind(strsplit(as.character(coef(fit))," ",fixed=TRUE)))
  h <- unlist(h)
  h <- data.frame(cbind((strsplit(as.character(h),'"',fixed=TRUE))))
  colnames(h) <- i
  modelsCoef <- cbind(modelsCoef,h)
  
  # make predictions
  predic <- predict(fit,testSet[,-10],type="response")
  
  # convert classifications to binary ONLY
  pr <- ifelse(predic>0.5,1,0)
  
  # form the confusion matrix - pr is rows and test is columns
  n <- data.frame(table(pr,testSet$visit))
  
  # store the model prediction results
  predTable <- cbind(predTable,n[,3])
}
  # Since not has less than 9246 records left, simply take all remaining records as no
  no <- not
  
  # randomly select training & testing set from Non-Visited customers
  pos1 <- sample(nrow(no),size=floor((nrow(no)/10)*7),replace=FALSE)
  trainNo <- no[pos1,]
  testNo <- no[-pos1,]
  
  # create distinct and non-repeatable bags for Non-visited customers
  training_positions <- sample(nrow(vis), size=nrow(no), replace=FALSE)
  train1 <-1:nrow(vis) %in% training_positions
  visit <- not[train1,]
  
  # randomly seect training & testing set from Visited customers
  pos <- sample(nrow(visit),size=floor((nrow(visit)/10)*7),replace=FALSE)
  train<- visit[pos,]
  test<- visit[-pos,]
    
  # combine the train & test Bags of both Visit & Non-Visit customers
  trainSet <- rbind(train,trainNo)
  testSet <- rbind(test,testNo)
  
  fit <- glm(visit~., data=trainSet, family=binomial)
  h <- data.frame(cbind(strsplit(as.character(coef(fit))," ",fixed=TRUE)))
  h <- unlist(h)
  h <- data.frame(cbind((strsplit(as.character(h),'"',fixed=TRUE))))
  #colnames(h) <- i
  modelsCoef <- cbind(modelsCoef,h)

  # make predictions
  predic <- predict(fit,testSet[,-10],type="response")

  # convert classifications to binary ONLY
  pr <- ifelse(predic>0.5,1,0)

  # form the confusion matrix - pr is rows and test is columns
  n <- data.frame(table(pr,testSet$visit))

  # store the model prediction results
  predTable <- cbind(predTable,n[,3])


# clear the first column (dummy) from modelsCoef
modelsCoef[,1] <- NULL

# ModelsCoef is currently in list and character format - with "" for each value
# Hereby convert it to a numeric data frame for further usage
h <- as.numeric(unlist(modelsCoef))
dim(h) <- c(10,6)
modelsCoef <- data.frame(h)

predTable <- data.frame(predTable)

error1<-sqrt((sum((as.numeric(testSet$visit)-predic)^2))/nrow(testSet))


# set the predtable row names for easier identification
rownames(predTable) <- c("0,0","1,0","0,1","1,1")

# get rid of surplus variables
rm(h,pos,sel,pos1,n,no,pr,predic)
