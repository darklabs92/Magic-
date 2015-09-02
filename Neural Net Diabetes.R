require(caTools)
require(nnet)
require(caret)

setwd("F:\\ISS\\CI 1\\CI")

# read the Diabetes data file
data <- read.csv("Diabetes.csv",header=TRUE)


# understand what data says
#str(data)

d <- data

# convert output class into a factor
# d1 <- as.factor(d$out)

# split the test set into Train & Test
set.seed(1000)
check <- sample.split(d$out, SplitRatio=0.75)
train1 <- subset(d,check==TRUE)
trOut <- as.numeric(train1[,9])
train <- train1[,-9]
test1 <- subset(d,check==FALSE)
tstOut <- as.numeric(test1[,9])
test <- test1[,-9]

# train the neural net
nn <- nnet(out~.,data=train1, na.action=na.omit, size=5, rang=0.1, maxit=250)

# use the model on test set
pr <- predict(nn, test1)
pr <- round(pr,0)

# confusion table
#table(pr,test1$out)
# NN (MLP) on Diabetes in R
confusionMatrix(pr,test1$out)