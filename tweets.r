#install.packages(c("devtools", "rjson", "bit64", "httr"))
library(devtools)
#1install_github("twitteR", username="geoffjentry")
library(twitteR)
#install.packages("plyr")
library(plyr)
#install.packages("tm")
library(tm)
# download the wordcloud generating package
#install.packages(c("wordcloud","tm"),repos="http://cran.r-project.org")
library("wordcloud")

#Setting up the OAuth Key
api_key <- "TJNQXDA1rGZwTTL7JPoOc6KLj"

api_secret <- "HDYeVpKdeWMNQkwLFRxMkxnFNC0GSemML1oCVYS3a4LjaKokTF"

access_token <- "16280903-JPPOkKbNzZCiupElwzKDFPeV7BXxXS632rVVLCpao"

access_token_secret <- "4LKo4TJGejrGYwAbg7NRrRQeUcaXBzBNsz2da9JNxQcpy"

setup_twitter_oauth(api_key,api_secret)

#Setup is now complete

#This is a search query wherein we search for a searchString [iphone in this case]. searchString has to be provided, other params not so 
searchTwitter("iphone")

#n = no of tweets to be returned
#resultType returns both popular as well as real time / recent results
# print tweets to view the same
tweets = searchTwitter("#singapore", n=2000, resultType="mixed")

# we need to make sense of all the unstructured data. Thus, we create a function on the fly which gets the text and apply it 
#to the stored tweets.
tweets.text = laply(tweets,function(t)t$getText())




# Now, this extracted text must first be cleaned in order to perform further analysis of any type.
# We now define a function called clean.text() in order to do so recursively for us.

clean.text <- function(some_txt)
{
  some_txt = gsub("&amp", "", some_txt)
  
  some_txt = gsub("(RT|via)((?:\b\\W*@\\w+)+)", "", some_txt)
  
  some_txt = gsub("@\\w+", "", some_txt)
  
  some_txt = gsub("[[:punct:]]", "", some_txt)
  
  some_txt = gsub("[[:digit:]]", "", some_txt)
  
  some_txt = gsub("http\\w+", "", some_txt)
  
  some_txt = gsub("[ t]{2,}", "", some_txt)
  
  some_txt = gsub("^\\s+|\\s+$", "", some_txt)
  
  # define "tolower error handling" function
  
  try.tolower = function(x)
    
  {
    
    y = NA
    
    try_error = tryCatch(tolower(x), error=function(e) e)
    
    if (!inherits(try_error, "error"))
      
      y = tolower(x)
    
    return(y)
    
  }
  
  some_txt = sapply(some_txt, try.tolower)
  
  some_txt = some_txt[some_txt != ""]
  
  names(some_txt) = NULL
  
  # now, we return the cleaned text in the tweet - that is this text is free of generic programming punctuation and syntax
  return(some_txt)
  
}

# now, we implement the afore-defined function
clean_text = clean.text(tweets.text)

tweet_corpus = Corpus(VectorSource(clean_text))

tdm = TermDocumentMatrix(tweet_corpus,control = list(removePunctuation = TRUE,stopwords = c("machine", "learning", stopwords("english")),removeNumbers = TRUE, tolower = TRUE))


m = as.matrix(tdm) #we define tdm as matrix

word_freqs = sort(rowSums(m), decreasing=TRUE) #now we get the word orders in decreasing order

dm = data.frame(word=names(word_freqs), freq=word_freqs) #we create our data set

pal <- brewer.pal(9,"BuGn")
pal <- pal[-(1:4)]

# time to generate the Final WordCloud!
wordcloud(dm$word, dm$freq, random.order=FALSE, colors=pal)


# the following saves the generated word cloud to a PNG file
png("Cloud.png", width=12, height=8, units="in", res=300)

wordcloud(dm$word, dm$freq, random.order=FALSE, colors=brewer.pal(8, "Dark2"))

dev.off()