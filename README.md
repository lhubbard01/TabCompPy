# TabCompPy
This is meant to be used as a tab completion utility tool for python programs. I am rather inexperienced with tab completion scripts, but I found this helpful. I might be wrong in assuming that all tab completable files for python must be executable on their own, i.e. containing a "#!/usr/bin/python" preprocessor directive, but for the time being, thats how the program expects the file to behave. 

To set a python file to be executable, simply add a preprocessor directive like the one mentioned above at the head of the file. For posix systems, "chmod +x \_\_filename\_\_", with the preprocessor directive should be sufficient. I don't know how windows works. 

At any rate, this is useful for python programs with many parameters processed through the argparse module. For experiments run with many commandline parameters, parameter paths can be useful. e.g. --data.loc xyz --model.name MODEL --model.location x\y\z . 
These can be easily listed through the tabcomppy command.

