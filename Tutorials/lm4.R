y <- rnorm(10,0,1)

poll = read.csv("C:\\Users\\Trost\\Desktop\\AIWebScaleData\\pollsdata.txt",header = TRUE,sep=" ")
library(lme4)  # load library

a  = lmer(bush ~ 1+(1|state),data=poll,family=binomial(link="logit"))

