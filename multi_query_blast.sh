#!/bin/bash
programname=$0
function usage {
    echo "usage: $programname [-h] fasta_query_directory genome_blastdb"
    echo "performs blastp search of each query in the query directory on the given genome"
    echo "  -h      display help"
    echo "arguments:"
    echo "  1. fasta_query_directory        directory containing fasta queries "
    echo "  2. path_to_genome_blastdb       path to the genome blastdb to be queiried against"
    exit 1
}
if [ "$1" == "-h" ]
then
    usage
fi
if [ $# -eq 0 ]
then
    echo "no arguments supplied. Need fasta_query_directory, genome_blastdb"
    usage
fi
outDir="./reciprical_blast_results"
 mkdir $outDir 
 queries=$(ls $1)
 for file in $queries
 do
 path=${1}/${file}
 echo "querying ${path} agianst ${2}"
 blastp -query ${path} -db ${2} -num_descriptions 5 -num_alignments 5 -out ${outDir}/${file}_rblast.txt
 done