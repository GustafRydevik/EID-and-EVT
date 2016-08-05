autolib<-function(Package,mirror="http://stat.ethz.ch/CRAN",...){
  if(!suppressWarnings(require(as.character(substitute(Package)),
                               character.only=TRUE,quietly=TRUE,...))){
    Package<-as.character(substitute(Package))
    install.packages(Package,repos=mirror,...)
    library(Package,character.only=TRUE)
  }
}
autolib(readxl)
autolib(dplyr)
autolib(stringr)
autolib(extRemes)
data.path<-"./outbreak-data/smith-rsi-outbreakdata"
smith_database<-read_excel(file.path(data.path,"SmithEtAl_outbreakdata.xlsx"))
names(smith_database)<-str_replace(names(smith_database)," ",".")
smith_database<-smith_database%>%filter(Total.Cases!=9999)
smith_database<-as.data.frame(smith_database)
smith_database<-smith_database[,-9]

#some specific disease extracts
smith_cholera<-smith_database%>%filter(Disease== "CHOLERA")
smith_meningitis_bact<-smith_database%>%filter(Disease=="MENINGITIS - BACTERIAL")
smith_meningitis_viral<-smith_database%>%filter(Disease=="MENINGITIS - ASEPTIC (VIRAL)")
smith_nipah<-smith_database%>%filter(Disease=="NIPAH AND NIPAH-LIKE VIRUS DISEASE" )
smith_plague<-smith_database%>%filter(Disease== "PLAGUE")
smith_wnv<-smith_database%>%filter(Disease=="WEST NILE FEVER")
smith_rvf<-smith_database%>%filter(Disease=="RIFT VALLEY FEVER")
smith_tularemia<-smith_database%>%filter(Disease== "TULAREMIA")