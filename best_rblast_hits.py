#!/usr/bin/env python

import argparse
import pandas as pd
import json
import os


def main():
    description=''
    rblast_dir_description="This dir contains all blast results from the reciprocal blast"
    dir_json='directory to store json file containing all rblast best hits'
    default_path = os.getcwd() + '/best_rblast_hits.csv'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-rblast_dir",help=rblast_dir_description, type=str, required=True)
    parser.add_argument("-out", help="path for output file",type=str, required=False, default=default_path )
    #parser.add_argument("-prot_ids", nargs='+', help="proteins", required=True, )
    parser.set_defaults(func=run)
    args=parser.parse_args()
    args.func(args)
    

def run(args):
    print(args)
    best_hits_dict = best_hit_to_dict(args.rblast_dir)
    #num_hits_dict = count_hits_mapped_to_protein(best_hits_dict, args.prot_ids)
    #df = pd.DataFrame(num_hits_dict.values(), num_hits_dict.keys())
    
    df = pd.DataFrame(best_hits_dict.values(), best_hits_dict.keys())
    df.to_csv(args.out)
    
    

def best_hit_to_dict(path_to_rblast_results):
    """Return a dict {accession:protein_id} with the accession of genome and the best hit in the source genome"""
    
    files =os.listdir(path_to_rblast_results)
    paths = [os.path.join(path_to_rblast_results,file) for file in files]
    #paths = fu.get_filepaths_in_dir(path_to_rblast_results) 
    best_hits_dict = {}
    for path in paths:
        line_of_interest = None
        accession = path.split('/')[-1][:15]
        with open(path, 'r') as f:
            for i,line in enumerate(f):
                if line.startswith('>'):
                    prot_id = line.split(' ')[0][1:]
                    best_hits_dict[accession]=prot_id
    return best_hits_dict
    

def save_besthits_json(path_to_dir, best_hits_dict):
    """Save a json file from the best hits dict in the directory of your choosing"""

    path_json_hit_dict = os.path.join(path_to_dir,'./best_hit.json' )
    if not os.path.exists(path_json_hit_dict):
        with open(path_json_hit_dict, 'w') as f:
            json.dump(best_hits_dict, f)
    else: print(f'the file {path_json_hit_dict} already exists.')
    
    
    
def count_hits_mapped_to_protein(best_hits_dict, protein_ids):
    """Return a dict containing the protein and the number of blast searches which it was the best hit"""
    
    df = pd.DataFrame(best_hits_dict.values(), best_hits_dict.keys())
    df.columns=['rblastp_best_hit']
    #astA protein_IDs in A.baumannii 17978-mff (genbank) 
    num_hits = {}
    for prot in protein_ids:
        num_hits['total'] = df.shape[0]
        filt_df = df['rblastp_best_hit']==prot
        num_hits[prot] = sum(filt_df)
    return num_hits
    
    


if __name__ == "__main__":
    main()