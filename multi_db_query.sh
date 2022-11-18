#!/usr/bin/env bash
programname=$0
function usage {
    echo "usage: $programname [-h] lst_assembly_accessions query_file database_dir"
    echo "performs blastp search with input query on each blast database indicated in the assembly accession text"
    echo "  -h      display help"
    echo "arguments:"
    echo "  1. lst_assembly_accessions  list of assembly accessions, should be corresponding blast databases in database_dir"
    echo "  2. query_file               fasta file containing a single fasta sequence to be queried against each database in accessions"
    echo "  3. database_dir             path to the directory containing the blast databases"
    exit 1
}

if [ "$1" == "-h" ]
then
    usage
fi

if [ $# -eq 0 ]
then
    echo "no arguments supplied. Need list of assembly accessions, query_file, and blast database_dir"
    usage
fi
#blast query sequence against each blast db (from accession list) and return output file for each set of hits

accessions_file=$1
query_file=$2
database_dir=$3
outDir="./hits_for_each_genome"
mkdir $outDir
while read line; do
    echo "reading accession: ${line}"
    echo $query_file
    blastp -query $query_file -db ${database_dir}/${line}/${line}_db -num_descriptions 5 -num_alignments 5 -out ${outDir}/${line}_blastpOut.txt
    echo ${database_dir}/${line}/${line}_db
done < $accessions_file