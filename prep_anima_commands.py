"""Provides bash script for running non linear registration

    Example: python prep_anima_commands.py -r vol_0000.nii.gz -s vol_000*.nii.gz

    """

import os 
import argparse
from copy import copy 


def load_args(): 
    parser = argparse.ArgumentParser()
    parser.add_argument('-r','--reference_image', type=str, required=True, help='provide the volume with least motion. Please provide relative or full path')
    parser.add_argument('-s', '--source', type=str, nargs='+', help='image, or list of images, to register. e.g. can use regexp like vol_00*.nii.gz')
    args = parser.parse_args()
    
    return args 

if __name__=="__main__":
    
    args = load_args()
    
    assert os.path.exists(args.reference_image)
    for s in args.source:
        assert os.path.exists(s)

    cmd_base = ["docker", "run", 
           "-v", "$PWD:/data", 
           "sergeicu/anima:latest", 
           "/anima/animaDenseSVFBMRegistration"]
    cmds = []
    for s in args.source: 
        output = s.replace(".nii.gz", "_r.nii.gz")
        
        # compose docker run commands 
        cmd = copy(cmd_base)
        cmd.extend(["-r", "/data/"+args.reference_image, 
                    "-m", "/data/"+s,
                    "-o","/data/"+output, 
                    "-O", "/data"+output.replace(".nii.gz", "_tr.nii.gz"), 
                    "-p","3", 
                    "-l", "0",
                    "&>", "log_"+s.replace(".nii.gz", ""), "&"])
        cmds.append(cmd)

    # write docker commands to file 
    savefile = "non_rigid_docker_commands.sh"
    with open(savefile, "w") as f:
        _ = [i.append("\n") for i in cmds]
        cmds = [" ".join(i) for i in cmds]
        f.writelines(cmds)
        
    print(f"bash {savefile}")
    
