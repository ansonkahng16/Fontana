#you might need to install this package in your version of R.
library("rms");

#change this to your working directory
# setwd("D:\\work\\demographic_toy")
setwd("/Users/ansonkahng/Fontana/R")

#load the data from disk
chloroquine_deaths <- read.csv("2014_07_25_incubator_4_chloroquine_2.csv");

#The bj code has a hard time interpreting the Event.Frequency column, so we expand
#the data so that each row is a single death.
ns_convert_frequencies_into_repeats<- function(raw_data,frequency_column="Event.Frequency"){
	temp = raw_data[rep(row.names(raw_data), raw_data[,frequency_column]), 1:ncol(raw_data)];
	temp[,frequency_column][temp[,frequency_column]>1] = 1;
	return(temp)
}
chloroquine_deaths = ns_convert_frequencies_into_repeats(chloroquine_deaths);

#set up the data type for easy plotting later on.
chloroquine_deaths$concentration = as.double(as.character(chloroquine_deaths$Environmental.Conditions))
	
#Assign each individual a label the AFT algorithm will then interpret as a categorical variable
chloroquine_deaths$bj_group =  factor(paste(chloroquine_deaths$concentration,
					    chloroquine_deaths$Plate.Name,sep=":"));
				
#chose an arbitrary group among animals unexposed to choloroquine to use as a reference group
bj_reference_label = chloroquine_deaths$bj_group[chloroquine_deaths$concentration==0][1]


#set up the categorical variable for the AFT,
#so that the algorithm will know to use the 
#chosen reference group.
groups = levels(chloroquine_deaths$bj_group)
bj_reference_level = which(groups == bj_reference_label)				
num_groups = length(groups)
contrasts(chloroquine_deaths$bj_group) <- contr.treatment(num_groups,base=bj_reference_level);	

#solve the AFT model using the Buckley James method.
#A good read might be http://www.ncbi.nlm.nih.gov/pmc/articles/PMC2583435/
ret_prop  <- bj(Surv(chloroquine_deaths$Age.at.Death..d..Raw,
		1-chloroquine_deaths$Censored)~chloroquine_deaths$bj_group,
		x=TRUE, y=TRUE)

#get the residuals
r_prop <- resid(ret_prop, type="censored")
chloroquine_deaths$bj_residual = exp(r_prop[,1]);


##We might want to consider the actual coefficients for each group (as opposed to the residuals)
##The default labels in the bj coefficient table aren't reliable, so we need to reconstruct this table.
coeff_labels = c(as.character(bj_reference_label),groups[groups!=bj_reference_label])
n = as.character(coeff_labels)
p =regexpr(":",n)-1;
n[p!=-2] = substring(n[p!=-2],0,p[p!=-2])
n = as.double(n);
scaling = data.frame(group=coeff_labels,concentration=n,coeff=exp(ret_prop$coefficients))
rownames(scaling) = NULL;
#zero out the refernce group (to which bj assigns the model intercept)
scaling$coeff[1]=1; 

#count the number of individuals in each group.
agg <- aggregate(data=chloroquine_deaths, chloroquine_deaths$Age.at.Death..d..Raw ~ chloroquine_deaths$bj_group, function(x) length(unique(x)))
names(agg) = c("bj_group","N")
scaling$N = "";
for (j in 1:(dim(agg)[1])){
	scaling[scaling$group==as.character(agg$bj_group[[j]]),"N"] = agg$N[[j]];
}

scaling$N = as.double(scaling$N)

#plot the original data
par(mfrow=c(2,2),mar=c(4,4,.5,.5));
s = survfit(Surv(chloroquine_deaths$Age.at.Death..d..Raw,
		1-chloroquine_deaths$Censored)~chloroquine_deaths$bj_group)
conc = substring(names(s$strata),29,30)
conc[conc=="0:"] = "0";
colors = rep("black",length(conc));
colors[conc==16]="green";
colors[conc==32]="red";
plot(s,col=colors,mark.time=F,xlab="time (days)",ylab="S[t]")
legend("topright",title="[chloroquine]",
        legend=c(0,16,32),col=c("black","green","red"),lty=1,bty="n")

#plot regression model coefficients
colors = rep("black",length(scaling$concentration));
colors[scaling$concentration==16]="green";
colors[scaling$concentration==32]="red";
plot(scaling$concentration,scaling$coef,
     log="y",col=colors,
     xlab="[chloroquine]",ylab="AFT model coefficient")
legend("topright",title="[chloroquine]",
        legend=c(0,16,32),col=c("black","green","red"),lty=1,bty="n")

#plot regression model residuals
s = survfit(Surv(chloroquine_deaths$bj_residual,
		1-chloroquine_deaths$Censored)~chloroquine_deaths$bj_group)
conc = substring(names(s$strata),29,30)
conc[conc=="0:"] = "0";
colors = rep("black",length(conc));
colors[conc==16]="green";
colors[conc==32]="red";
plot(s,col=colors,mark.time=F,xlab="residual time (days)",ylab="S[t]")
legend("topright",title="[chloroquine]",
        legend=c(0,16,32),col=c("black","green","red"),lty=1,bty="n")

#plot aggregated model residuals
s = survfit(Surv(chloroquine_deaths$bj_residual,
		1-chloroquine_deaths$Censored)~chloroquine_deaths$concentration)
conc = substring(names(s$strata),34,35)
colors = rep("black",length(conc));
colors[conc==16]="green";
colors[conc==32]="red";
plot(s,col=colors,mark.time=F,xlab="residual time (days)",ylab="S[t]")
legend("topright",title="[chloroquine]",
        legend=c(0,16,32),col=c("black","green","red"),lty=1,bty="n")
