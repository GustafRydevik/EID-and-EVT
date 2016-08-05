autolib<-function(Package,mirror="http://stat.ethz.ch/CRAN",...){
  if(!suppressWarnings(require(as.character(substitute(Package)),
                               character.only=TRUE,quietly=TRUE,...))){
    Package<-as.character(substitute(Package))
    install.packages(Package,repos=mirror,...)
    library(Package,character.only=TRUE)
  }
}
autolib(rfigshare)


ebola_outbreaks_detailed<-read.csv(url("https://ndownloader.figshare.com/files/3230399"),header=T,sep=",")
library(dplyr)
ebola_outbreaks_detailed%>%
  group_by(str_replace(OB_ID,"[a-z]",""))%>% ## changing OB_ID-s 11a, ... 11d to 11,and grouping by each outbreak code.
  filter(UNIQ_ID==min(UNIQ_ID))->ebola_outbreaks ## Keeping the earliest ID within each outbreak
