#!/usr/bin/env bash
programname=$0
function usage {
    echo "usage: $programname [-h] lst_assembly_accessions query_file database_dir proteome_dir parent_genome"
    echo "description"
    echo "1) use query fasta proteon sequence to blastp each database in database dir"
    echo "2) Get the best hit from each blast search and turn that into a query for rblastp"
    echo "3) blast each best hit agianst the parent genome of the original query"
    echo "  -h      display help"
    echo "arguments:"
    echo "  1. lst_assembly_accessions  list of assembly accessions, should be corresponding blast databases in database_dir"
    echo "  2. query_file               fasta file containing a single fasta sequence to be queried against each blast database database indicated in the accessions file"
    echo "  3. database_dir             path to the directory containing the blast databases"
    echo "  4. proteome_dir             path to the directory containing the proteomes from which to make rblast query protein fasta"
    echo "  5. parent_genome            path to the base file name in the parent genome blast db"
    exit 1
}

if [ "$1" == "-h" ]
then
    usage
fi

if [ $# -eq 0 ]
then
    echo "no arguments supplied"
    usage
fi



assembly_accessions=$1
query_protein=$2
blastp_database=$3
proteomes=$4
parent_genome=$5


echo $assembly_accessions
#blastp query against each blast database 
# args: accessions, query, blast_database_dir
bash ./multi_db_query.sh $assembly_accessions $query_protein $blastp_database


#make fasta file for best hit to use as quwery in reciprocal blast
#args: proteome_dir
python3 ./make_queries.py -proteomes $proteomes -bbhits ./hits_for_each_genome

#blastp each best hit agains parent genome
bash ./multi_query_blast.sh ./top_hits $parent_genome