if(!require(readr)) {
  install.packages("readr"); require(readr)}
if(!require(nnet)) {
  install.packages("nnet"); require(nnet)}
if(!require(caTools)) {
  install.packages("caTools"); require(caTools)}
if(!require(caret)) {
  install.packages("caret"); require(caret)}
if(!require(foreach)) {
  install.packages("foreach"); require(foreach)}
if(!require(doParallel)) {
  install.packages("doParallel"); require(doParallel)}
if(!require(e1071)) {
  install.packages("e1071"); require(e1071)}

#read in the data set
a <- read_delim("C:\\Users\\A0136039H\\Downloads\\Data Analytics\\data.csv", col_names=TRUE, delim=',')

a <- data.frame(a)

# ensure the target binomial variables are factors for classification
a$visit <- factor(a$visit)
a$conversion <- factor(a$conversion)


# Phase 1 - Visit classificaion
#
#
#
# remove Cust. ID, history, mens, womens, combo, conversion, spend and DM_category
b <- a[,-c(1,4,5,6,7,13,14,15)]

# select people who visited and who did not visit separately
vis <- b[which(b$visit==1),]              # 9246 rows
notf <- not <- b[which(b$visit!=1),]      # 53753 rows

# define the no. of bags to create and run for
iter <- 30
predLogTable <- predSVM <- modelSVMCoef <- predic <- NULL
modelSVMCoef <- modelLogCoef <- data.frame(rep(0,7))
accLog <- accSVM <- data.frame(rep(NULL,2))
#Bagging iterations
for (i in 1:iter) {
  # randomly select training & testing set from Visited customers
  pos <- sample(nrow(vis),size=floor(nrow(vis)/10*8),replace=FALSE)
  train<- vis[pos,]
  test<- vis[-pos,]
  
  # create distinct and non-repeatable bags for Non-visited customers
  sel <- sample(nrow(not), size=ifelse(nrow(not)>=floor(53753/6),floor(53753/6),nrow(not)), replace=FALSE)
  #train1 <-1:nrow(not) %in% sel
  no <- not[sel,]
  
  # randomly select training & testing set from Non-Visited customers
  pos1 <- sample(nrow(no),size=floor((nrow(no)/10)*8),replace=FALSE)
  trainNo <- no[pos1,]
  testNo <- no[-pos1,]
  
  # combine the train & test Bags of both Visit & Non-Visit customers
  trainSet <- rbind(train,trainNo)
  testSet <- rbind(test,testNo)
  
  svmfit1 <- svm(x=trainSet[,-7],y=factor(trainSet[,7]), kernel="radial", cost=5)
  modelSVMCoef <- cbind(modelSVMCoef,svmfit1)
  
  
  #------ logistic regression model build ---------
  #
  #
  #
  Logfit <- glm(visit~., data=trainSet, family=binomial)
  
  # make Logistic predictions
  predic <- predict(Logfit,newdata=testSet[,-7],type="response")
  
  
  h <- data.frame(cbind(strsplit(as.character(coef(Logfit))," ",fixed=TRUE)))
  h <- unlist(h)
  h <- data.frame(cbind((strsplit(as.character(h),'"',fixed=TRUE))))
  colnames(h) <- i
  modelLogCoef <- cbind(modelLogCoef,h)
  
  # convert classifications to binary ONLY
  pr <- ifelse(predic>0.5,1,0)
  
  # form the confusion matrix - pr is rows and test is columns
  n <- data.frame(table(pr,testSet$visit))
  
  # store the model prediction results
  predLogTable <- cbind(predLogTable,n[,3])
  
  # --------- End of Logistic Model Build ----------- #
  
  
  # --------- NN model build -----------------------  #
  #
  svmfit1 <- svm(x=trainSet[,-7],y=factor(trainSet[,7]), kernel="radial", cost=5)
  
  # make Logistic predictions
  predic <- predict(svmfit,newdata=testSet[,-7],type="response")
  
  
  h <- data.frame(cbind(strsplit(as.character(coef(svmfit))," ",fixed=TRUE)))
  h <- unlist(h)
  h <- data.frame(cbind((strsplit(as.character(h),'"',fixed=TRUE))))
  colnames(h) <- i
  modelLogCoef <- cbind(modelLogCoef,h)
  
  # convert classifications to binary ONLY
  pr <- ifelse(predic>0.5,1,0)
  
  # form the confusion matrix - pr is rows and test is columns
  n <- data.frame(table(pr,testSet$visit))
  
  # store the model prediction results
  predLogTable <- cbind(predLogTable,n[,3])
  
  
  # --------- End of NN Model Build ----------------  #
  
  # replenish the not visited data frame after every 5 runs
  ifelse(i%%6 == 0, not <- notf, not <- not[-sel,])
} 

# clear the first column (dummy) from modelsCoef
modelLogCoef[,1] <- NULL

# ModelsCoef is currently in list and character format - with "" for each value
# Hereby convert it to a numeric data frame for further usage
h <- as.numeric(unlist(modelLogCoef))
dim(h) <- c(7,iter)
modelLogCoef <- data.frame(h)

predLogTable <- data.frame(predLogTable)

#error1<-sqrt((sum((as.numeric(testSet$visit)-predic)^2))/nrow(testSet))

# determine the accuracy and sensitivity for Logistic
for (i in 1:iter) {
  accLog[1,i] <- (predLogTable[1,i]+predLogTable[4,i]) / (predLogTable[1,i]+predLogTable[2,i]+predLogTable[3,i]+predLogTable[4,i])
  accLog[2,i] <- predLogTable[4,i]/(predLogTable[4,i]+predLogTable[3,i])
}

# set the predtable row names for easier identification
rownames(predLogTable) <- c("0,0","1,0","0,1","1,1")
rownames(accLog) <- c('Acc.','Sensitivity')
# get rid of surplus variables

# Make final prediction for visit 

n <- as.integer(sample(1:iter,1))
x <- 1:iter
x <- x[-n]
k <- c(1,2,3,5)

vistart <- sys.time()

final <- data.frame(rep(2,length(x)))
fin <- NULL
t <- testSet
t1 <- trainSet
t2 <- rbind(trainSet,testSet)
t$predVisit <- NULL
t1$predVisit <- NULL
t2$predVisit <- NULL
for(l in 1:nrow(b)) {
  for(i in x) {
    pred=0
    for(j in k) {
      pred = pred+modelLogCoef[j,i]*as.numeric(b[l,j])
    }
    #print(pred)
    pred=exp(pred)
    pred = round(pred/(1+pred))
    fin <- rbind(fin,pred)  
  }
  b[l,8] <- round(mean(fin))
  fin <- NULL
}
viend <- sys.time()
vitime = vistart - viend
confusionMatrix(b[,8],b[,7])

a$predVisit = b[,8]

rm(h,pos,sel,pos1,pr,predic,final,no,not,notf,t,t1,t2,test,testNo,train,trainNo,vis,i,iter,j, k, l,predNN, x)

#              Reference
#Prediction     0     1
#         0 22434  4759
#         1 31319  4487
#
#     Accuracy : 0.4273
#
#     Sensitivity : 0.4174          
#     Specificity : 0.4853 

# --------------- End of Phase 1 -------------------- #


# --------------- Start of Phase 2------------------- #

#
#
#
# remove Cust. ID, history, combo, visit, spend and DM_category
c <- a[,-c(1,4,7,12,14,15)]

# select only the columns which have been predicted to 
c <- c[which(c$predVisit==1),]

# select people who converted and who did not convert separately
vis <- c[which(c$conversion==1),]              # 262 rows      243 rows
notf <- not <- c[which(c$conversion!=1),]      # 37234 rows    35204 rows

# define the no. of bags to create and run for
iter <- 3*ceiling(nrow(notf)/nrow(vis))
conPredLogTable <- conpredNN <- modelNNCoef <- predic <- NULL
conModelLogCoef <- data.frame(rep(0,10))
conAccLog <- conAccNN <- data.frame(rep(NULL,2))
#Bagging iterations
for (i in 1:iter) {
  # randomly select training & testing set from Converted visitors
  pos <- sample(nrow(vis),size=floor(nrow(vis)/10*8),replace=FALSE)
  train<- vis[pos,]
  test<- vis[-pos,]
  
  # create distinct and non-repeatable bags for Non-converted visitors
  sel <- sample(nrow(not), size=ifelse(nrow(not)>=floor(nrow(notf)/nrow(vis)),floor(nrow(notf)/nrow(vis)),nrow(not)), replace=FALSE)
  #train1 <-1:nrow(not) %in% sel
  no <- not[sel,]
  
  # randomly select training & testing set from Non-Visited customers
  pos1 <- sample(nrow(no),size=floor((nrow(no)/10)*8),replace=FALSE)
  trainNo <- no[pos1,]
  testNo <- no[-pos1,]
  
  # combine the train & test Bags of both Visit & Non-Visit customers
  trainSet <- rbind(train,trainNo)
  testSet <- rbind(test,testNo)
  
  #------ logistic regression model build ---------
  #
  #
  #
  Logfit <- glm(conversion~., data=trainSet, family=binomial)
  
  # make Logistic predictions
  predic <- predict(Logfit,newdata=testSet[,-9],type="response")
  
  
  h <- data.frame(cbind(strsplit(as.character(coef(Logfit))," ",fixed=TRUE)))
  h <- unlist(h)
  h <- data.frame(cbind((strsplit(as.character(h),'"',fixed=TRUE))))
  colnames(h) <- i
  conModelLogCoef <- cbind(conModelLogCoef,h)
  
  # convert classifications to binary ONLY
  pr <- ifelse(predic>0.5,1,0)
  
  # form the confusion matrix - pr is rows and test is columns
  n <- data.frame(table(pr,testSet$conversion))
  
  # store the model prediction results
  predLogTable <- cbind(predLogTable,n[,3])
  
  # --------- End of Logistic Model Build ----------- #
  
  
  # --------- NN model build -----------------------  #
  
  
  
  # --------- End of NN Model Build ----------------  #
  
  # replenish the not visited data frame after every 5 runs
  ifelse(i%%145 == 0, not <- notf, not <- not[-sel,])
} 

# clear the first column (dummy) from modelsCoef
conModelLogCoef[,1] <- NULL

# ModelsCoef is currently in list and character format - with "" for each value
# Hereby convert it to a numeric data frame for further usage
h <- as.numeric(unlist(conModelLogCoef))
dim(h) <- c(10,iter)
conModelLogCoef <- data.frame(h)

predLogTable <- data.frame(predLogTable)

error1<-sqrt((sum((as.numeric(testSet$visit)-predic)^2))/nrow(testSet))

# determine the accuracy and sensitivity for Logistic
for (i in 1:iter) {
  accLog[1,i] <- (predLogTable[1,i]+predLogTable[4,i]) / (predLogTable[1,i]+predLogTable[2,i]+predLogTable[3,i]+predLogTable[4,i])
  accLog[2,i] <- predLogTable[4,i]/(predLogTable[4,i]+predLogTable[3,i])
}

# set the predtable row names for easier identification
rownames(predLogTable) <- c("0,0","1,0","0,1","1,1")
rownames(accLog) <- c('Acc.','Sensitivity')
# get rid of surplus variables

# Make final prediction for visit 

n <- as.integer(sample(1:iter,1))
x <- 1:iter
x <- x[-n]
k <- c(1,2,3,4,5,7)

c[,11] <- NULL
final <- data.frame(rep(2,length(x)))
fin <- NULL
#t <- testSet
#t1 <- trainSet
#t2 <- rbind(trainSet,testSet)
#t$predVisit <- NULL
#t1$predVisit <- NULL
#t2$predVisit <- NULL
for(l in 1:nrow(c)) {
  for(i in x) {
    pred=0
    for(j in k) {
      pred = pred+conModelLogCoef[j,i]*as.numeric(c[l,j])
    }
    #print(pred)
    pred=exp(pred)
    pred = round(pred/(1+pred))
    fin <- rbind(fin,pred)  
  }
  c[l,11] <- round(mean(fin))
  fin <- NULL
}
confusionMatrix(c[,11],c[,9])

