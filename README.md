# project-template

Template to create data science projects for field site analysis with the 
MiBiPreT tools and beyond.

## Using this template

1. **Please _do not fork this repository directly on GitHub._** Instead,
   use GitHub's function to copy this template repository and customize it for
   your workshop. On this page (<https://github.com/MiBiPreT-FieldSites/project-template>),
   click on the blue _'Use this template'_ button (top right) and select 
   _'Create a new repository'_.

2. Select the owner for your new repository. Typically this is the `MiBiPreT-FieldSites` GitHub organisation.

3. Choose a name for your repository, ideally reflecting the field site you analyse.

4. Make sure the repository is public, leave "Include all branches" unchecked.
   Click on "Create repository from template". You will be redirected to
   your new repository.

5. Adapt the CITATION.cff file with your own details. You can use
   [the online tool](https://citation-file-format.github.io/cff-initializer-javascript) to
   create the content for the file and copy it in or use the update functionality.

## Workflow

1. Make use of branching and pull request, instead of directly modifying the main branch.

2. Adapt the preliminary structure to your project needs. Populate with your files and
   remove template files. 

3. Update the `README.md`. It should contain information that will help anyone, including
   a future version of yourself to understand why this project exists, how things are 
   organized (repository structure), where they can find more information and anything else you want to specify.

4. Add significant intermediate steps and/or after finalizing your work, tag the 
   repository with a version like `v1.0`. When you have activated that [Zenodo](https://zenodo.org/) 
   trackes your repository, a Zenodo release will be created, so you can cite the repository in your publication.


## Structure

### Basic structure
We suggest to organize your repository in the given structure:
- `data/` - *here you place your input data (add subfolders, if appropriate, see below)*
    - data.csv
- `docs/` - *Markdown-files containing your documentation*
    - doc.md
- `notebooks/` - *here your examples notebooks are stored (add subfolders, if appropriate)*
     - prototype-notebook.ipynb
- `results/` - *here your computed results and plots are stored (add subfolders, if appropriate)*
    - results.csv
- `scripts/`  - here place all your python scripts
    - `analysis/` - *all scripts for data analysis, modelling etc, ideally in the form of functions and classes*
        - analysis.py
    - `data/` - *all scripts for data manipulation, such loading, clean-up, preprocessing*
        - data.py 
    - `tests/` - *scripts to test your main functionality (from `analysis/`)*
        - test_analysis.py
    - `visualize/` - *scripts for data and results visualization (e.g. figures in publications)*
        - visualize.py
- CITATION.cff - specify your credentials for citation here
- environment.yml
- LICENSE - the default license is Apache 2.0, you can use another one if wanted
- README.md - please describe your project in the readme, including specification of all files

The suggested structure is not the ultimate way to organizing a repository. It 
should be adapted to the project specifics and requirements. 

### Extensions

We suggest possible extensions, such as
* adding archive folder with scripts and data no longer in use, e.g.
    - `notebooks/`
        - prototype-notebook.ipynb
        - `archive/`
               -no-longer-useful.ipynb
        - `figures/`
            - Fig_01.png
            - Fig_02.png        
* substructuring your data, such as
    - `data/`
        - `raw/`
        - `processed/`
        - `cleaned/`
* if you work with additional software which requires input files, e.g. bash-scripts 
  for working on cluster, ModFlow input files etc, create a new folder for these 
  scripts, e.g. within the script-folder:
    - `scripts/`  
        - `bash/` - bash scripts for cluster work
    

## Sources

This template has been designed with input from other repository templates, such as
https://github.com/GeoStat-Examples/template and the GitHub Gist column 
*How to organize your Python data science project* 
(https://gist.github.com/ericmjl/27e50331f24db3e8f957d1fe7bbbe510)
