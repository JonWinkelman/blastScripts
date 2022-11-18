#!/usr/bin/env bash
programname=$0
function usage {
    echo "usage: $programname [-h] lst_assembly_accessions proteome_dir"
    echo "Makes a blast database for each proteome (given by list of ass. accession) in the proteoem directory"
    echo "  -h      display help"
    echo "arguments:"
    echo "  1. lst_assembly_accessions  list of assembly accessions, should be corresponding proteomoes in proteome_dir"
    echo "  2. proteome_dir             dir containint proteomes. Shoould be assembly accession with appended .faa"
    exit 1
}

if [ "$1" == "-h" ]
then
    usage
fi

if [ $# -eq 0 ]
then
    echo "no arguments supplied. Need list of assembly accession and the proteome dir"
    usage
fi
dir1=./blast_databases
mkdir $dir1
#read in list of accessions
filename=$1
proteome_dir=$2
n=1
while read line; do
# reading each line
echo "reading accession No. ${n} : ${line}"
mkdir ${dir1}/${line}
makeblastdb -in ${2}/${line}.faa -dbtype 'prot' -out ./${dir1}/${line}/${line}_db
echo "made blast db: ./${line}/${line}_db"
n=$((n+1))
done < $filename