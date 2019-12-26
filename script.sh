#!/usr/bin/env bash
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install docker.io -y
sudo docker login -u username -p password
sudo docker service start
sudo docker pull biocontainers/blast:v2.2.31_cv2
mkdir blast_example
cd blast_example
sudo wget http://www.uniprot.org/uniprot/P04156.fasta
sudo curl -O ftp://ftp.ncbi.nih.gov/refseq/D_rerio/mRNA_Prot/zebrafish.1.protein.faa.gz
sudo gunzip zebrafish.1.protein.faa.gz
sudo docker run -v `pwd`:/data/ biocontainers/blast:v2.2.31_cv2 makeblastdb -in zebrafish.1.protein.faa -dbtype prot
sudo docker run -v `pwd`:/data/ biocontainers/blast:v2.2.31_cv2 blastp -query P04156.fasta -db zebrafish.1.protein.faa -out results.txt
less results.txt