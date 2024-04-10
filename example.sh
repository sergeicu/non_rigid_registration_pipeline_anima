# what this repo does 
1. resample all files to isotropic 
2. non rigid registration via anima 


# what you need to provide 
1. list of files to resample - either as a list or via *.nii.gz like regexp 
2. a file with the least motion - e.g. the first b0 or b50 image in the series


# what this repo does NOT do 
1. even-odd registration. If you want to add this - just chain it with this - https://github.com/sergeicu/odd_even_reg



# example run 
cd data 
python ../resample_to_isotropic.py -s vol_000*.nii.gz 
bash resampling_docker_commands.sh
python ../prep_anima_commands.py -r vol_0000_iso.nii.gz -s vol_000*_iso.nii.gz 
bash non_rigid_docker_commands.sh


# install dependencies: 
- python 
- crkit docker image (available on ganymede or gamakchi; see below for custom install instructions) 

# warning!!! 
the intensity values of your files need to be more than 1! If they are in the range of 0-1 the registration will not work. 

# CRKIT Docker
    To perform isotropic resampling (as shown in example.sh) 
    Make sure that crkit docker image is installed. It is currently installed on `ganymede` machine. 
    To pull crkit docker to any other machine - you can find it here - 
    `docker pull ccts3.aws.chboston.org:5151/computationalradiology/crkit`
    if you do not have access to BCH internal `ccts3` website - make sure you ask someone who has 
    you will need to go to ccts3.aws.chboston.org with your BCH account, then generate a API token, then perform docker login with it... it is rather complicated if you haven't done it before
