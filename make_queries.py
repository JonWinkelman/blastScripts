#!/usr/bin/env python

from jw_utils import parse_fasta as pfa
from jw_utils import file_utils as fu
import os
import argparse

#get the protein sequence for the top hit in each genome
# path_to_blastpOut = './hits_for_each_genome'
# proteome_dir = './Proteomes'
# best_hit_dict_tot = write_best_hit_queries(proteome_dir, path_to_blastpOut)

#proteome_dir,path_to_blastpOut, query_dir=None
def write_best_hit_queries(args):
    """Write each best hit to its own fasta file
    parameters:
    proteome_dir (str): path to the proteome directory
    path_to_blastpOut (str): path to directory contianin output from initial blast
    query_dir (str): path to dir that you want to create to store the created fasta files

    return (dict, nested): { assembly_accession:{protein_id:sequence} }
    """

    best_hit_dict_tot = get_sequence(args.proteomes, args.bbhits)
    if not args.query_dir:
        args.query_dir = './top_hits'
    os.makedirs(args.query_dir)
    for acc, seq_dict in best_hit_dict_tot.items():
        with open(os.path.join(args.query_dir,f'{acc}.faa'), 'w') as f:
            for prot_id, seq in seq_dict.items():
                f.write(f'>{prot_id}\n')
                f.write(f'{seq}\n')
    return best_hit_dict_tot


def make_besthit_dict(path_to_blastpOut):
    """return a dict {accession:protein_ID} with best blast hit for each genome in the output dir"""
    paths = fu.get_filepaths_in_dir(path_to_blastpOut)
    line_of_interest=None
    best_hit_dict = {}
    for path in paths:
        with open(path, 'r') as f:
            accession = path.replace(path_to_blastpOut+'/','')[:15]
            for i, line in enumerate(f):
                if line.startswith('Sequences producing significant alignments:'):
                    line_of_interest = i+2
                if i==line_of_interest:
                    best_hit_dict[accession]=line.split(' ')[0]
    return best_hit_dict


def get_sequence(proteome_dir, path_to_blastpOut):
    """return {accession:{protein_ID:seq}} for each best hit    """
    best_hit_dict = make_besthit_dict(path_to_blastpOut)
    #get protein seq for each best hit
    best_hit_dict_tot = {}
    for acc, prot_id in best_hit_dict.items():
        proteome_path = os.path.join(proteome_dir, f'{acc}.faa')
        d = pfa.get_seq_dict(proteome_path)
        seq = d.get(prot_id, None)
        best_hit_dict_tot[acc] = {prot_id:seq}
        if not seq:
            print(acc, prot_id)
    return best_hit_dict_tot



def best_hit_to_dict(path_to_rblast_results):
    """Return a dict with the accession of query genome and the best hit in the source genome

    These are the results of the reciprical blast. For each genome, there was a best hit in the initial
    blastp. This best hit was reciprical blasted against the genome containing the original query. If best
    hit in this reciprical blastp is the initial query, then these proteins are likely orthologs.
    
    return (dict): {accession:protein_id}  
    """
    paths = fu.get_filepaths_in_dir(path_to_rblast_results) 
    d = {}
    for path in paths:
        line_of_interest = None
        accession = path.split('/')[-1][:15]
        with open(path, 'r') as f:
            for i,line in enumerate(f):
                if line.startswith('>'):
                    prot_id = line.split(' ')[0][1:]
                    d[accession]=prot_id
                    print(prot_id)
    return d


def main():
    description='From a directory of blast output files, write best hit from each file to its own fasta file'
    proteome_dir_description="This dir contains all proteome files. Sequence for each fasta file will be pulled from these proteomes"
    
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-proteomes",help=proteome_dir_description, type=str, required=True)
    parser.add_argument("-bbhits", help="directory containing output files from initial blast", required=True)
    parser.add_argument("-query_dir", help="path to directory that will contain output", required=False, default=None)
    parser.set_defaults(func=write_best_hit_queries)
    args=parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
    #proteome_dir = '/Users/jonwinkelman/Dropbox/Trestle_projects/Palmer_lab/baumannii_blast_db/Proteomes'
    #blastp_out = '/Users/jonwinkelman/Dropbox/Trestle_projects/Palmer_lab/utilities/hits_for_each_genome'
    #d = write_best_hit_queries(proteome_dir=proteome_dir, path_to_blastpOut=blastp_out)