# import the twitteR library for use
if(!require(twitteR)) {
  install.packages("twitteR"); require(twitteR)}
# import the smappR library in case of use
if(!require(smappR)) {
  require(devtools);install_github("SMAPPNYU/smappR"); require(smappR)}

# set the authentication keys of 4 different apps for usage
ckey <- c("","","","")
csecret <- c("","","","")
atoken <- c("","","","")
asecret <- c("","","","")

# choose any of the apps ofr usage - range the indice from 1 to 4
consumerKey <- ckey[1]
consumerSecret <- csecret[1]
access_token <- atoken[1]
access_token_secret <- asecret[1]

# establish the authentication handshake
setup_twitter_oauth(consumerKey,consumerSecret,access_token,access_token_secret)

read_file <- read.csv("C:\\Users\\Vidyut Singhania\\Downloads\\New_Business_Cases\\twitter_research\\Twitter\\AirBnB_post_timelineFeb.csv",stringsAsFactors = FALSE)

colnames((read_file))

# determine the unqiue twitter handles from the provided file
speakr <- as.list(unique(read_file[,"replyToSN"]))
speakr=speakr[!is.na(speakr)]
speakr1 = speakr
nxt <- r <- 1 
for (i in nxt:length(speakr1)){
  r <- r+1
  dest = "C:\\Users\\Vidyut Singhania\\Downloads\\twitter\\profile\\"
  now <- paste(dest,speakr[i],sep="")
  now <- paste(now,"txt",sep=".")
  tl <- getTimeline(filename = now,screen_name = speakr[i],n=3200,verbose=TRUE,oauth_folder = "C:\\Users\\Vidyut Singhania\\Downloads\\New_Business_Cases\\twitter_research\\Twitter\\ibt2")
  nxt<- r
}

# collect the tweets for the interacted users

r <- 0
m<-1
#finTime <- data.frame(stringsAsFactors = F)
o <- unique(finTime$screenName)
while(length(unique(o))<length(speakr)){
  if(m<4) {
    m<-m+1
  }
  else{
    m<-1
  }
  consumerKey <- ckey[m]
  consumerSecret <- csecret[m]
  access_token <- atoken[m]
  access_token_secret <- asecret[m]
  
  setup_twitter_oauth(consumerKey,consumerSecret,access_token,access_token_secret)
  
  speakr1 <- speakr[length(unique(o))+1:length(unique(o))+41]
  nxt <- 1
  for (i in nxt:length(speakr1)){
    r <- r+1
    tweets <- try(userTimeline(speakr[i],n=3200,includeRts = TRUE),silent=TRUE)
    if(!(inherits(tweets ,'try-error'))){
      finTime <- rbind(finTime,twListToDF(tweets))  
    }
    nxt<- r
  }
  
}

write.csv(finTime,"C:\\Users\\Vidyut Singhania\\Downloads\\twitter\\profile\\status.csv")
