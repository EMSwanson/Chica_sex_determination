rm(list=ls())

###

#setwd("C:/Users/Owner/OneDrive/School/Data, analyses/ChicaPopGen/Sex chromosome analysis/Hets files and database/")
setwd("E:/OneDrive/School/Data, analyses/ChicaPopGen/Sex chromosome analysis/Hets files and database/")


Molino <- read.csv("Molino.csv")
names(Molino)[1] <- "Scaffold"

CaballoMoro <- read.csv("CaballoMoro.csv")
names(CaballoMoro)[1] <- "Scaffold"

Chica <- read.csv("Chica.csv")
names(Chica)[1] <- "Scaffold"

Sexes <- read.csv("Sexes.csv")
names(Sexes)[1] <- "ID"

#With big file sizes, can use these functions to get a good sense of the data without opening the whole dataset
names(Molino)
head(Molino)
summary(Molino)
str(Molino)
dim(Molino)
nrow(Molino)
ncol(Molino)

###Looking at small numbers of rows and data frame characteristics
head(merge(Molino,Chica),10)
dim(merge(Molino,Chica))

###Checking that scafcounter is the same for every group
Molino[Molino[,1] == "KB872436.1",]
CaballoMoro[CaballoMoro[,1] == "KB872436.1",]
Chica[Chica[,1] == "KB872436.1",]

fishes <- merge(Chica,merge(Molino,CaballoMoro,by="Scaffold"))
dim(fishes)

###Female IDs
Sexes[Sexes$Sex=="F",]$ID

###Many ways to do this, such as intersect(), match(), and others.
fishes$fem_mean<- rowMeans(fishes[names(fishes) %in% Sexes[Sexes$Sex=="F",]$ID])
fishes$mal_mean<- rowMeans(fishes[names(fishes) %in% Sexes[Sexes$Sex=="M",]$ID])

###means div by scafcounter, using scafcounter.y because it has less 0s ??? 
fishes$fem_mean_possible <- fishes$fem_mean/fishes$Scafcounter.y
fishes$mal_mean_possible <- fishes$mal_mean/fishes$Scafcounter.y

fishes$mal_var<- apply((fishes[names(fishes) %in% Sexes[Sexes$Sex=="M",]$ID]),MARGIN = 1, FUN = var)
fishes$fem_var<- apply((fishes[names(fishes) %in% Sexes[Sexes$Sex=="F",]$ID]),MARGIN = 1, FUN = var)

fishes$fem_min_mal <- fishes$fem_mean_possible - fishes$mal_mean_possible

fishes_lowFemVar_hiMalVar<- fishes[fishes$fem_var <= 5 & fishes$mal_var >= 20,]
ordered_fishes_lowFemVar_hiMalVar <- fishes_lowFemVar_hiMalVar[order(fishes_lowFemVar_hiMalVar$fem_var),]

fishes_hiFemVar_lowMalVar<- fishes[fishes$mal_var <= 5 & fishes$fem_var >= 20,]
ordered_fishes_hiFemVar_lowMalVar <- fishes_hiFemVar_lowMalVar[order(fishes_hiFemVar_lowMalVar$fem_var),]

write.csv(ordered_fishes_lowFemVar_hiMalVar$Scaffold,file="Scaffs with low female variance and hi male variance.csv")
write.csv(ordered_fishes_hiFemVar_lowMalVar$Scaffold,file="Scaffs with high female variance and low male variance.csv")

