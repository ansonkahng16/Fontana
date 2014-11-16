#you might need to install this package in your version of R.
library("rms");

#change this to your working directory
setwd("/Users/ansonkahng/Fontana/R")

#load the data from disk
# model_data <- read.csv("../data/wk4/testdata_highcutoff.csv");
model_data <- read.csv("../data/wk5/testdata.csv");

#Assign each individual a label the AFT algorithm will then interpret as a categorical variable
# use model_data$name

#chose an arbitrary group among animals unexposed to choloroquine to use as a reference group
bj_reference_label = model_data$name[model_data$name=='r_5000_100_0.01_0_0'][1]
# ^ hardcoded in; change later please

#set up the categorical variable for the AFT,
#so that the algorithm will know to use the 
#chosen reference group.rm
groups = levels(model_data$name)
bj_reference_level = which(groups == bj_reference_label)
num_groups = length(groups)
contrasts(model_data$name) <- contr.treatment(num_groups,base=bj_reference_level);


#solve the AFT model using the Buckley James method.
#A good read might be http://www.ncbi.nlm.nih.gov/pmc/articles/PMC2583435/
ret_prop  <- bj(Surv(model_data$fpt,1-model_data$alive)~model_data$name,
                x=TRUE, y=TRUE)

#get the residuals
r_prop <- resid(ret_prop, type="censored")
model_data$bj_residual = exp(r_prop[,1]);


##We might want to consider the actual coefficients for each group (as opposed to the residuals)
##The default labels in the bj coefficient table aren't reliable, so we need to reconstruct this table.
coeff_labels = c(as.character(bj_reference_label),groups[groups!=bj_reference_label])
n = as.character(coeff_labels)
p =regexpr(":",n)-1;
n[p!=-2] = substring(n[p!=-2],0,p[p!=-2])
n = as.double(n);
scaling = data.frame(group=coeff_labels,coeff=exp(ret_prop$coefficients))
rownames(scaling) = NULL;
#zero out the reference group (to which bj assigns the model intercept)
scaling$coeff[1]=1; 

#count the number of individuals in each group.
agg <- aggregate(data=model_data, model_data$fpt ~ model_data$name, function(x) length(unique(x)))
names(agg) = c("bj_group","N")
scaling$N = "";
for (j in 1:(dim(agg)[1])){
  scaling[scaling$group==as.character(agg$bj_group[[j]]),"N"] = agg$N[[j]];
}

scaling$N = as.double(scaling$N)

#plot the original data
par(mfrow=c(2,2),mar=c(4,4,.5,.5));

s = survfit(Surv(model_data$fpt,1-model_data$alive)~model_data$name)
conc = substring(names(s$strata),17,40)  # get name
colors = rep("black",length(conc));
colors[conc=='r_5000_100_0.01_0_0']="green";
colors[conc=='sf_5000_100_0.01_0_0']="red";
# colors[conc=='r_5000_100_0.02_0_0']="blue";
# colors[conc=='sf_5000_100_0.02_0_0']="orange";
# colors[conc=='r_2500_100_0.01_0_0']="cyan";
# colors[conc=='sf_2500_100_0.01_0_0']="magenta";
# colors[conc=='r_2500_100_0.02_0_0']="pink";
# colors[conc=='sf_2500_100_0.02_0_0']="purple";
# colors[conc=='r_2500_100_0.05_0_0']="yellow";
# colors[conc=='sf_2500_100_0.05_0_0']="gray";
# colors[conc=='r_50000_100_0.01_0_0']="black";
# colors[conc=='sf_50000_100_0.01_0_0']="black";
plot(s,col=colors,mark.time=F,xlab="time (days)",ylab="S[t]")
# legend("topright",#title="[Simulation Data]",
#        legend=c('r/5000/0.01','sf/5000/0.01','r/5000/0.02',
#                 'sf/5000/0.02','r/2500/0.01','sf/2500/0.01',
#                 'r/2500/0.03','sf/2500/0.02','r/2500/0.05',
#                 'sf/2500/0.05','r/50000/0.01','sf/50000/0.01'),
#        col=c("green","red","blue",
#              "orange","cyan","magenta",
#              "pink","purple","yellow",
#              "gray","black","black"),lty=1,bty="n")

#plot regression model coefficients
plot(scaling$group,scaling$coef)  # also fix later...log plot?

# colors = rep("black",length(scaling$concentration));
# colors[scaling$concentration==16]="green";
# colors[scaling$concentration==32]="red";
# plot(scaling$concentration,scaling$coef,
#      log="y",col=colors,
#      xlab="[chloroquine]",ylab="AFT model coefficient")
# legend("topright",title="[chloroquine]",
#        legend=c(0,16,32),col=c("black","green","red"),lty=1,bty="n")


#plot regression model residuals
s = survfit(Surv(model_data$bj_residual,
                 1-model_data$alive)~model_data$name)

conc = substring(names(s$strata),17,40)  # get name
colors = rep("black",length(conc));
colors[conc=='r_5000_100_0.01_0_0']="green";
colors[conc=='sf_5000_100_0.01_0_0']="red";
# colors[conc=='r_5000_100_0.02_0_0']="blue";
# colors[conc=='sf_5000_100_0.02_0_0']="orange";
# colors[conc=='r_2500_100_0.01_0_0']="cyan";
# colors[conc=='sf_2500_100_0.01_0_0']="magenta";
# colors[conc=='r_2500_100_0.02_0_0']="pink";
# colors[conc=='sf_2500_100_0.02_0_0']="purple";
# colors[conc=='r_2500_100_0.05_0_0']="yellow";
# colors[conc=='sf_2500_100_0.05_0_0']="gray";
# colors[conc=='r_50000_100_0.01_0_0']="black";
# colors[conc=='sf_50000_100_0.01_0_0']="black";
plot(s,col=colors,mark.time=F,xlab="time (days)",ylab="S[t]")
# legend("topright",#title="[Simulation Data]",
#        legend=c('r/5000/0.01','sf/5000/0.01','r/5000/0.02',
#                 'sf/5000/0.02','r/2500/0.01','sf/2500/0.01',
#                 'r/2500/0.03','sf/2500/0.02','r/2500/0.05',
#                 'sf/2500/0.05','r/50000/0.01','sf/50000/0.01'),
#        col=c("green","red","blue",
#              "orange","cyan","magenta",
#              "pink","purple","yellow",
#              "gray","black","black"),lty=1,bty="n")

#plot aggregated model residuals
s = survfit(Surv(model_data$bj_residual,
                 1-model_data$alive)~model_data$name)

conc = substring(names(s$strata),17,40)  # get name
colors = rep("black",length(conc));
colors[conc=='r_5000_100_0.01_0_0']="green";
colors[conc=='sf_5000_100_0.01_0_0']="red";
# colors[conc=='r_5000_100_0.02_0_0']="blue";
# colors[conc=='sf_5000_100_0.02_0_0']="orange";
# colors[conc=='r_2500_100_0.01_0_0']="cyan";
# colors[conc=='sf_2500_100_0.01_0_0']="magenta";
# colors[conc=='r_2500_100_0.02_0_0']="pink";
# colors[conc=='sf_2500_100_0.02_0_0']="purple";
# colors[conc=='r_2500_100_0.05_0_0']="yellow";
# colors[conc=='sf_2500_100_0.05_0_0']="gray";
# colors[conc=='r_50000_100_0.01_0_0']="black";
# colors[conc=='sf_50000_100_0.01_0_0']="black";
plot(s,col=colors,mark.time=F,xlab="time (days)",ylab="S[t]")
# legend("topright",#title="[Simulation Data]",
#        legend=c('r/5000/0.01','sf/5000/0.01','r/5000/0.02',
#                 'sf/5000/0.02','r/2500/0.01','sf/2500/0.01',
#                 'r/2500/0.03','sf/2500/0.02','r/2500/0.05',
#                 'sf/2500/0.05','r/50000/0.01','sf/50000/0.01'),
#        col=c("green","red","blue",
#              "orange","cyan","magenta",
#              "pink","purple","yellow",
#              "gray","black","black"),lty=1,bty="n")
