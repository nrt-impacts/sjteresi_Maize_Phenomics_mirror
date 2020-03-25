# Maize_Phenomics
Module 2 Maize Phenomics in-class project

Please place the `ground_data_2019.csv`, `point_data_6in_2019obs.csv` and the `obs_2019_key.csv` file in the Maize_Phenomics/data/ directory. I have updated the gitignore to not track these files.

I have hard-coded in the names inside the main code section `phenomics.py`. There I create a config file and read from that to assign the filenames. Alternatively I could've hard-coded that in for each import script but I thought it made more sense to put it in `phenomics.py`. I also thought it would be easier on everyone if we refrained from command-line arguments because that would be a little harder to understand than the config file, but we can discuss as a group if that would be something people would like to explore.
