library(openxlsx)
library(corrgram)
require(caTools)
require(e1071)

a <- read.csv("F:\\ISS\\Semester 2\\Assignments\\Data Analytics\\trial.csv", header=TRUE)

# --------------------------- #
# Phase 1
#
# 
b <- a[,1:13]

# final data set to be used for Phase 1 Logistic Regression
c <- b[,-c(1,4,12,13)]


# split into train and test
set.seed(1000)
check <- sample.split(c, SplitRatio=0.75)
trainSet <- subset(c,check==TRUE)
testSet <- subset(c,check==FALSE)


# Train Set w/o target 
e <- as.matrix(trainSet[,1:8])

# Train target variable
d <- factor(trainSet$visit)


# correlation matrix for data set
cor(b)

# visual represetnation of the Correlation mat.
corrgram(b)



glm.out <- glm(visit~history_segment_binned+mens+womens+zip_code_binned+segment_binned, family=binomial(logit), data=trainSet)

summary(glm.out)

# Test Set
f <- as.matrix(testSet[,1:8])
# Test Target
g <- factor(testSet$visit)

pr <- predict(glm.out,newdata = as.data.frame(f), type = "response")
table(round(pr),g)



# DEFAULT SVM Model applied
set.seed(1000)
default <- svm(visit~history_segment_binned+mens+womens+zip_code_binned+segment_binned,trainSet)
pr <- predict(default,testSet)
table(round(pr),testSet$visit)
