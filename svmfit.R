library(e1071)
set.seed(1)
x=matrix(rnorm(20*2),ncol=2)
y=c(rep(-1,10),rep(1,10))

x[y==1,]=x[y==1,]+1
plot(x, col=(3-y))

#linear SVM 
dat=data.frame(x=x, y=as.factor(y))
svmfit=svm(y~., data=dat,kernel="linear", cost = 10, scale = F)
svmfit
#plots the model
plot(svmfit,dat)
# Index Gives the Support Vectors which help the model determine the hypersphere / hyperplane / line 
svmfit$index

summary(svmfit)
str(svmfit)


svmfit=svm(y~.,data=dat, kernel="linear", cost = 0.1, scale = F)
plot(svmfit, dat)

svmfit$index
svmfit

set.seed(1)
tune.out=tune(svm,y~.,data=dat,kernel="linear", ranges=list(cost=c(0.001,0.01,0.1,1,5,10,100)))

summary(tune.out)

bestmod=tune.out$best.model
summary(bestmod)

xtest=matrix(rnorm(20*2), ncol=2)
ytest=sample(c(-1,1), 20, rep=T)
xtest[ytest==1,]=xtest[ytest==1,]+1
testdat=data.frame(x=xtest, y=as.factor(ytest))

ypred=predict(bestmod, testdat)
table(predict=ypred, truth=testdat$y)

svmfit=svm(y~., data=dat, kernel="linear", cost=0.01, scale=F)
ypred=predict(svmfit, testdat)
table(predict=ypred, truth=testdat$y)

x[y==1,]=x[y==1,]+0.5
plot(x, col=3-y, pch=19)

dat=data.frame(x=x, y=as.factor(y))
svmfit=svm(y~., data=dat, kernel="linear", cost=1e5)
summary(svmfit)
plot(svmfit, dat)

set.seed(1)
x=matrix(rnorm(200*2), ncol=2)
x[1:100,]=x[1:100,]+2
x[101:150,]=x[101:150,]-2
y=c(rep(1,150),rep(2,50))
dat=data.frame(x=x, y=as.factor(y))

plot(x, col=y+1)

train=sample(200,100)
svmfit=svm(y~.,data=dat[train,], kernel="radial", gamma=1, cost=1)
plot(svmfit, dat[train,])

summary(svmfit)


svmfit=svm(y~.,data=dat[train,], kernel="polynomial", gamma=1, cost=1e5)
plot(svmfit, dat[train,])


set.seed(1)
tune.out=tune(svm,y~.,data=dat,kernel="radial", ranges=list(cost=c(0.1,1,10,100,1000)))

summary(tune.out)

# Obtain feature weights
w= t(svmfit$coefs) %*% svmfit$SV
t(svmfit$coefs) %*% svmfit$SV

head(svmfit$decision.values)
