library(caTools)
library(grnn)
library(caret)

setwd("F:\\ISS\\CI 1\\CI")

data = read.csv("Diabetes.csv", header=TRUE)

size=nrow(data)

length=ncol(data)

index <- 1:size
data$out <- as.numeric(data$out)
check <- sample.split(data$out,SplitRatio=0.75)

training <- subset(data,check==TRUE)
testing <- subset(data,check==FALSE)
result <- testing
testing <- testing[,1:length-1]
result$actual = result[,length]
result$predict = -1

nn <- learn(training, variable.column=length)
nn <- smooth(nn, sigma = 0.9)


for(i in 1:nrow(testing))
{  
  vec <- as.matrix(testing[i,])
  res <- guess(nn, vec)
  res <- round(res,0)
  
  if(is.nan(res))
  {
    cat("Entry ",i," Generated NaN result!\n")
  }
  else
  {
    result$predict[i] <- res
  }
}



result.size = nrow(result)
result.correct = nrow(result[round(result$predict) == result$actual,])
# GRNN on Diabetes in R
cat("No of test cases = ",result.size,"\n")
cat("Correct predictions = ", result.correct ,"\n")
cat("Accuracy = ", result.correct / result.size * 100 ,"\n")

result2<- cbind(testing, data.frame(result))