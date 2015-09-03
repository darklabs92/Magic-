if(!require(readr)) {
  install.packages("readr"); require(readr)}
if(!require(tm)) {
    install.packages("tm"); require(tm)}
if(!require(SnowballC)) {
  install.packages("SnowballC"); require(SnowballC)}

#read in the data set
a <- read_delim("C:\\Users\\A0136039H\\Downloads\\music_survey.txt", col_names=TRUE, delim='\t')

#a <- data.frame(a)

# display the col names of the text doc
a[0,]

#tabulate the freq of the Product types in the text document 
table(a$Product)

# create a character vector which stores like_most
pos <- character(0)
pos <- a$like_most

# create a character vector which stores like_least
neg <- character(0)
neg <- a$like_least

# create the corpus (large document format) from tm package for the provided text
pos.corpus <- VCorpus(VectorSource(pos))

# remove white space
pos.corpus <- tm_map(pos.corpus,stripWhitespace)

#convert to lowercase
