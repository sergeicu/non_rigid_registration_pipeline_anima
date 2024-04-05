"""Provides bash script for running non linear registration

    Example: python prep_anima_commands.py -r vol_0000.nii.gz -s vol_000*.nii.gz

    """

import os 
import argparse
from copy import copy 


def load_args(): 
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--source', type=str, nargs='+', help='image, or list of images, to resample. e.g. can use regexp like vol_00*.nii.gz')
    args = parser.parse_args()
    
    return args 

if __name__=="__main__":
    
    args = load_args()
    
    files = []
    for s in args.source:
        assert os.path.exists(s)
        files.append(os.path.basename(s))
        

    cmd_base = ["docker", "run", 
           "-v", "$PWD:/data", 
           "ccts3.aws.chboston.org:5151/computationalradiology/crkit", 
           "crlResampleToIsotropic"]
    cmds = []
    for s in files: 
        output = s.replace(".nii.gz", "_iso.nii.gz")
        
        # compose docker run commands 
        cmd = copy(cmd_base)
        cmd.extend(["/data/"+s,
                    "bspline", 
                    "/data/"+output,
                    "&>", "log_"+s.replace(".nii.gz", "_resampling"), "&"])
        cmds.append(cmd)

    # write docker commands to file 
    savefile = "resampling_docker_commands.sh"
    with open(savefile, "w") as f:
        _ = [i.append("\n") for i in cmds]
        cmds = [" ".join(i) for i in cmds]
        f.writelines(cmds)
        
    print(f"bash {savefile}")
    