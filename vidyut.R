library(readr)
library(foreach)
library(doParallel)
library(caret)
library(caTools)

#read in the data set
a <- read_delim("F:\\ISS\\Semester 2\\Assignments\\Data Analytics\\vd.csv", col_names=TRUE, delim=";")

a <- data.frame(a)

# ensure the target binomial variables are factors for classification

a$visit <- factor(a$visit)
a$conversion <- factor(a$conversion)


# Phase 1 - Visit classificaion
# remove Cust. ID, conversion and spend
b <- a[,-c(1,12,13)]

# select people who visited and who did not visit separately
vis <- b[which(b$visit==1),]
notf <- no <- not <- b[which(b$visit!=1),]


# create parallel processing environment for 2 (TWO) processors
cl<-makeCluster(2)
registerDoParallel(cl)

iterations <- 3

k=f=1
predictions <- foreach(m=1:iterations, .combine=cbind) %dopar% {
    #if(m<6) {
    # randomly select training & testing set from Visited customers
    set.seed(k)
    pos <- sample(nrow(vis),size=floor(nrow(vis)/10*7),replace=FALSE)
    train<- vis[pos,]
    test<- vis[-pos,]
    k = k+1
    
    # create distinct and non-repeatable bags for Non-visited customers
    set.seed(k)
    sel <- sample(nrow(not), size=9246, replace=FALSE)
    #train1 <-1:nrow(not) %in% training_positions
    no <- not[sel,]
    not <- not[-sel,]
    k = k+1
    
    # randomly select training & testing set from Non-Visited customers
    set.seed(k)
    pos1 <- sample(nrow(no),size=floor((nrow(no)/10)*7),replace=FALSE)
    trainNo <- no[pos1,]
    testNo <- no[-pos1,]
    k = k+1
    
    # combine the train & test Bags of both Visit & Non-Visit customers
    set.seed(k)
    trainSet <- rbind(train,trainNo)
    testSet <- rbind(test,testNo)
    k = k+1
    
    set.seed(f)
    fit <- glm(visit~., data=trainSet, family=binomial(logit))
    f = f+1
    
    #pr <- 
    print(k)
    print(length(not))
    predict(fit,testSet[,-10])
    #pr <- rbind(pr,predict(fit,testSet[,-10]))
    
  }
  pred <- rowMeans(predictions)
  stopCluster(cl)

length(predictions)

#error<-sqrt((sum((testSet$visit-predictions)^2))/nrow(testSet))
