require(caTools)
require(e1071)
require(caret)

#setwd("C:\\Users\\A0136039H\\Downloads\\CI")

# read the Diabetes data file
data <- read.csv("Diabetes.csv",header=TRUE)


# understand what data says
str(data)

# convert output class into a factor
data$out <- as.factor(data$out)

# split the test set into Train & Test
set.seed(1000)
check <- sample.split(data$out, SplitRatio=0.75)
train <- subset(data,check==TRUE)
test <- subset(data,check==FALSE)

# DEFAULT SVM Model applied
set.seed(1000)
default <- svm(out~.,train)
pr <- predict(default,test)
# Diabetes Default SVM in R
confusionMatrix(pr,test$out)

#
# pr     0   1
#  0   115  31
#  1    10  36

# Linear SVM applied
set.seed(1000)
linear <- svm(out~., train, kernel="linear")
pr <- predict(linear, test)
# Diabetes Linear kernel SVM in R
confusionMatrix(pr,test$out)

#
# pr    0   1
#  0  114  32
#  1   11  35

# Polynomial SVM applied
set.seed(1000)
poly <- svm(out~., train, kernel="polynomial")
pr <- predict(poly,test)
# Diabetes Polynomial SVM in R
confusionMatrix(pr,test$out)

#
# pr    0   1
#  0  119  46
#  1    6  21

set.seed(1001)
tune.out <- tune(svm,out~.,data=train,ranges=list(cost=c(0.00001,0.001,0.054,0.3,0.86,1.5,7,49)))
# we find that best cost paramters = 0.86
linear <- svm(out~., train, kernel="linear", cost=0.86)
pr <- predict(linear, test) 
#table(pr,test$out)
# Diabetes Optimized Linear SVM in R
confusionMatrix(pr,test$out)
#
# pr    0   1
#  0  114  32
#  1   11  35