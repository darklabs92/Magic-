if(!require(swirl)) {
  install.packages("swirl"); require(swirl)}

# open & use the SWIRL package 
swirl()

# Select EDA -> Exploratory Graphs

# display the top 5 rows of the (US pollution) data set loaded into memory  
head(pollution)

# display the dimensions of the data set loaded
dim(pollution)

# pm25 -> vaariable containing the polution level for the respective county + state
# display the summary statistics [Mean + Quantiles(0,25,50,75,100)] regarding the data in question
summary(pollution$pm25)

# we store pollution$pm25 in ppm, for ease of further use
# use the 'quantile' fn to display (almost) same results as summary - note, quantile does not display the 'mean'
quantile(ppm)

# display the data in a boxplot, to get a better understanding
boxplot(ppm)
boxplot(ppm, col="blue")

# add a horizontal line to the existing graph (boxplot), indicating the US National Average Std (12)
abline(h=12)

# display the data in a histogram now
hist(ppm)
hist(ppm, col="green")

# add a 1-D grayscale representation to the histogram, which gives slightly more detailed info about the spread of data
rug(ppm)

# specify the number of buckets to split the given data into
hist(ppm, col="green",breaks=100)

# display the data points over the limit with a vertical line
abline(v=12, lwd=4, col="magenta")

# display the data set variable names
names(pollution)

# lets tabulate the split of the counties / states, by the region
reg <- table(pollution$region)

# display a 1-D graph (barplot) indicating the split, described above, with the Chart's Title 'Number of Countries in Each Region"
barplot(reg, col="wheat", main="Number of Counties in Each Region")

# plot a comparison of the data Pollution, based on the region, using two boxplots
boxplot(pm25~region, data=pollution, col="red")

# plot a comparison of the data Pollution, , using two histograms
# first, set up the Graph window to enable 2 rows of hist plots, in 1 col [mfrow(2,1)]. mar sets up the margins 
par(mfrow=c(2,1), mar=c(4,4,2,1))

# use the subset function to extract only those records which lie in the East Region  
east <- subset(pollution, region=="east")

# display the head (default, top 5 rows) of this subsetted data 
head(east)

# display the first histogram in the 1st row / space designated
hist(east$pm25, col="green")

# display the Second Historgram in the 2nd row
hist(subset(pollution, region=="west")$pm25, col="green")

# scatter plot of latitude and pollution
with(pollution, plot(latitude,pm25))

# draw a horizontal line of type 2 (dashed line) indicating the US National Average Standard
abline(h=12, lwd=2, lty=2)

# plot a scatter plot with 3 variables - latitude, ppm & region (indicated by color)
plot(pollution$latitude, ppm, col=pollution$region)

# plot two scatter plots, each representing the pollution in a distinct region
par(mfrow=c(1,2), mar=c(5,4,2,1))
west <- subset(pollution, region=="west")
plot(west$latitude, west$pm25, main="West")
abline(h=12, lty=3, lwd=2)
plot(east$latitude, east$pm25, main="East")
abline(h=12, lty=2, lwd=2)
