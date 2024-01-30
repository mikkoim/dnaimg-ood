library("ape")
library("Biostrings")
fb2 = as.DNAbin(readDNAStringSet("../notebooks/otus_fb2_align.fasta"))

JC69 = dist.dna(fb2, model="JC69", as.matrix=T)
write.table(JC69, file="jc69.csv", sep=",")

K80 = dist.dna(fb2, model="K80", as.matrix=T)
write.table(K80, file="k80.csv", sep=",")
