
# blastScripts
<br>

#### Example to determine if AstA2 ortholog exists in other strains

<img src="reciprocal_blast.png" alt="reciprocal blast">
<br>
These are bash and python scripts to perform reciprocal blast
dependencies:<br>
BLAST+  <a href="https://www.ncbi.nlm.nih.gov/books/NBK569861/#intro_Installation.MacOSX">Install</a>
<br>
<a href="https://www.ncbi.nlm.nih.gov/books/NBK279691/">BLAST+ user manual</a>
<br>
1) build individual local blast databases from proteomes<br>  
2) blasting each database with an input fasta protein<br>   
3) turning best hit in each of the results from 2) into an individual fasta for rblast<br>  
4) running each best hit from 3) against the genome containing the original query sequence<br>  
5) building csv for results in 4<br> 

## Building blastp databases:  
<br>
1) Get fasta-formatted proteomes and put each fasta file into a proteomes directory<br> 
2) use the script "make_blastdb_each_proteome.sh" to build blastp database from each proteome<br> 

$ ./make_blastdb_each_proteome.sh accessions proteome_directory<br>

3) The name of the database folder for each genome should be the genome identifier, in my case<br>
   I use the NCBI assembly accession (e.g. GCF_000000000.1). The files inside the database folder<br>
   will have a _db appended as well as a variable extension name (e.g. GCF_000000000.1_db.pdb)<br>