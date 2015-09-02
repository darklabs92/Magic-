require(caTools)
require(e1071)
require(caret)

setwd("C:\\Users\\A0136039H\\Downloads\\CI")

# read the Wine Quality data file
data <- read.csv("winequality-white.csv",header=TRUE)


# understand what data says
str(data)

# convert output class into a factor
data$quality <- as.factor(data$quality)

# split the test set into Train & Test
set.seed(1000)
check <- sample.split(data$quality, SplitRatio=0.75)
train <- subset(data,check==TRUE)
test <- subset(data,check==FALSE)

# DEFAULT SVM Model applied
set.seed(1000)
default <- svm(quality~.,train)
pr <- predict(default,test)
# Default SVM on Wine Quality in R
confusionMatrix(pr,test$quality)

#
# pr    3   4   5   6   7   8   9
#  3    0   0   0   0   0   0   0
#  4    0   2   2   0   0   0   0
#  5    3  24 211  90   8   0   0
#  6    2  14 151 430 159  28   1
#  7    0   1   0  30  53  16   0
#  8    0   0   0   0   0   0   0
#  9    0   0   0   0   0   0   0

# Linear SVM applied
set.seed(1000)
linear <- svm(quality~., train, kernel="linear")
pr <- predict(linear, test)
# Linear SVM on Wine Quality in R
confusionMatrix(pr,test$quality)

#
# pr    3   4   5   6   7   8   9
#  3    0   0   0   0   0   0   0
#  4    0   0   0   0   0   0   0
#  5    2  24 200  96   9   4   0
#  6    3  17 164 454 211  40   1
#  7    0   0   0   0   0   0   0
#  8    0   0   0   0   0   0   0
#  9    0   0   0   0   0   0   0

# Polynomial SVM applied
set.seed(1000)
poly <- svm(quality~., train, kernel="polynomial")
pr <- predict(poly,test)
# Polynomial SVM on Wine Quality in R
confusionMatrix(pr,test$quality)


set.seed(1001)
tune.out <- tune(svm,quality~.,data=train, kernel="polynomial",ranges=list(cost=c(0.00001,0.001,0.054,0.3,0.86,1.5,7,49)))
# we find that best cost paramters = 49 sum
set.seed(1001)
polynom <- svm(quality~., train, kernel="polynomial", cost=49)
pr <- predict(polynom, test)
# Optimized Poly SVM on Wine Quality in R
confusionMatrix(pr,test$quality)

#
# pr    3   4   5   6   7   8   9
#  3    0   0   0   2   0   0   0
#  4    0   5  11   5   0   0   0
#  5    3  24 178  61   7   0   0
#  6    2  12 168 439 149  23   1
#  7    0   0   6  41  57   8   0
#  8    0   0   1   2   6  13   0
#  9    0   0   0   0   1   0   0