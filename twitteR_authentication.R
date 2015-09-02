#install.packages(c("devtools", "rjson", "bit64", "httr"))
#RESTART R session!
library(devtools)

#install.packages("twitteR")
library(stringi)
library(twitteR)

api_key <- "TJNQXDA1rGZwTTL7JPoOc6KLj"

api_secret <- "HDYeVpKdeWMNQkwLFRxMkxnFNC0GSemML1oCVYS3a4LjaKokTF"

access_token <- "16280903-JPPOkKbNzZCiupElwzKDFPeV7BXxXS632rVVLCpao"

access_token_secret <- "4LKo4TJGejrGYwAbg7NRrRQeUcaXBzBNsz2da9JNxQcpy"

setup_twitter_oauth(api_key,api_secret)