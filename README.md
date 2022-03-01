# aws_sam_filewatcher
A script to handle copying minor changes to the SAM build folder without having to rebuild each time.

# Default 
When run without arguments, the script will detect all changes in the directory initially run in, and will assume the SAM build directory is at relative path: `./aws-sam/build/<directory_name>`

# Running
This script works based on the directory it is called from. So you are able to put into path or in your python modules folder. Then it can be run using
 `python -m sam_file_watcher`

# Arguments
Arguments that can be passed to the script can be seen by using the `-h` argument.