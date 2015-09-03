#install.packages(c("devtools", "rjson", "bit64", "httr"))
#RESTART R session!
library(devtools)

#install.packages("twitteR")
library(stringi)
library(twitteR)

api_key <- ""

api_secret <- ""

access_token <- ""

access_token_secret <- ""

setup_twitter_oauth(api_key,api_secret)
