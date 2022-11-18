#!/usr/bin/env bash
programname=$0
function usage {
    echo "usage: $programname [-h] lst_assembly_accessions query_file database_dir"
    echo "description"
    echo "  -h      display help"
    echo "arguments:"
    echo "  1. lst_assembly_accessions  list of assembly accessions, should be corresponding blast databases in database_dir"
    echo "  2. query_file               fasta file containing a single fasta sequence to be queried against each database in accessions"
    echo "  3. database_dir             path to the directory containing the blast databases"
    exit 1
}
#query each blast database with the in
/Users/jonwinkelman/scripts/blastScripts/multi_db_query.sh trimmed_accessions.txt AKQ27614_1_GCA_001077675_1.faa /Users/jonwinkelman/Dropbox/Trestle_projects/Palmer_lab/baumannii_blast_db/blast_databases

#make fasta file for best hit to use as quwery in reciprocal blast
/Users/jonwinkelman/scripts/blastScripts/make_queries.py -proteomes /Users/jonwinkelman/Dropbox/Trestle_projects/Palmer_lab/baumannii_blast_db/Proteomes -bbhits /Users/jonwinkelman/Dropbox/Trestle_projects/Palmer_lab/rblast_dedup_AstA2/hits_for_each_genome /Users/jonwinkelman/Dropbox/Trestle_projects/Palmer_lab/rblast_dedup_AstA2/best_