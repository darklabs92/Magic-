require(caTools)
require(nnet)
require(caret)

setwd("F:\\ISS\\CI 1\\CI")

# read the Wine Quality data file
data <- read.csv("winequality-white.csv",header=TRUE)

d <- data

# convert output class into a factor
# d1 <- as.factor(d$out)

# split the test set into Train & Test
# set.seed(1002)
check <- sample.split(d$quality, SplitRatio=0.75)
train1 <- subset(d,check==TRUE)
train1$quality <- as.factor(train1[,12])
train <- train1[,-12]
test1 <- subset(d,check==FALSE)
test1$quality <- as.factor(test1[,12])
test <- test1[,-12]


# train the neural net
nn <- nnet(quality~., data=train1, size=10, maxit=5000)

#model_nnet <- nnet(quality ~ ., data=train, size=10, maxit=5000)

pr <- predict(nn,test1,type="class")
# pr <- round(pr,0)

# confusion table
#table(pr,test1$quality)

#confusion matrix
#Wine MLP classification in R
confusionMatrix(pr,test1$quality)