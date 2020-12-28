#!/usr/bin/python3

import os
import re

#Patterns for path gen in completion options
START = re.compile(r"\s+self\.([\w][\w\d_]*)\s*=[\s]*[\/{]")
ARGS = re.compile(r"\s*[\"\']([\w][\d\w]*)[\"\']\s*:\s*[\"\'\d\w]+[\"\']*[,\s]*")
END = re.compile(r"\s*(})\s*")



#completion patterns
FLAG_SINGLE = "-"
FLAG_DOUBLE = "--"


def generate_completion_file(file: str, start: int = 0, end: int = 0, associated_filename: str = None):
  """ NOTE, requires a class titled DEFAULTS, containing a dictionary for mapping. This allows for an enforced 
  practice of expected arguments, associated paths, etc. 
  
  attributes are declared on initialization, of the form self.X = {...}, self.Y = {...}


  seeks all attributes as paths corresponding to different aspects of the training runtime""" 

  NO_START = (True if start == -1 else False)
  NO_END   = (True if end == 0 else False)
  
  associated_filename = (associated_filename if associated_filename is not None else file)

  bash_script = file.split(os.path.sep)[-1][:-3] + ".sh"


  COMPLETION_FILE_DATA_START = "# _" + bash_script[:-3] + " tab completion file\n"\
    + "_" + bash_script[:-3] + "() {\n"\
    + "  local cur\n"\
    + "  COMPREPLY=()\n"\
    + "  cur=${COMP_WORDS[COMP_CWORD]}\n"\
    + "  case \"$cur\" in\n"\
    + "    -*)\n"\
    + "    COMPREPLY=( $( compgen -W \""

  COMPLETION_FILE_DATA_END = "-- $cur ) );;\n    esac\n    return 0;\n\n"\
    + "complete -F _" + bash_script[:-3] + " -o filenames " + associated_filename + "\n"
  
  completion_file_data = COMPLETION_FILE_DATA_START
  completion_file_data = file_flags(file, start, end, completion_file_data)


  completion_file_data += "}" + COMPLETION_FILE_DATA_END

  with open(bash_script, "w") as f:
    f.write(completion_file_data)

  return completion_file_data


def file_flags(file: str, start: int, end: int, completion_file_data: str):

  stack_state = 0 #pda state
  FORBIDDEN_CHARACTERS = "!@#$%^&*()-|\\"
  OPEN  = "{"
  CLOSE = "}"

  with open(file, "r") as f:

    lines = f.readlines()

  i = -1
  while i < len(lines)-1:
    i += 1

    prepend = START.findall(lines[i])
    if prepend:
      stack_state += 1
      prepend = prepend[0]
      
      stack_state, completion_file_data, i = path_group(stack_state, prepend, completion_file_data, lines, i)

  completion_file_data += "\""
  return completion_file_data


def path_group(stack_state: int, prepend: str, completion_file_data: str, lines: list, i: int):
  """ generates the completion string corresponding to the path to the runtime attribute,
    e.g. self.data or self.data.filepaths, etc.

    @stack_state - strictly nonnegative integer representing depth in dictionary of attributes, for PDA
    @prepend - path to this depth, e.g. data, data.nested, data.nested.nestedmore, etc.
    @completion_file_data - contents for the autogen completion script.
    @lines - file contents from src file
    @i - index into lines list, necessary since will be iterated in these calls



    """

  while i < len(lines):
      line_attrs = ARGS.findall(lines[i]) 
      if line_attrs:
        for attr in line_attrs:
          completion_file_data += FLAG_DOUBLE + prepend + "." + attr + "  "

      i += 1
      if END.findall(lines[i]):
        stack_state -= 1
        return stack_state, completion_file_data, i

  if stack_state > 0:
      raise ValueError("Unclosed dictionary detected")

if __name__ == "__main__":
  import argparse
  parser = argparse.ArgumentParser()

  parser.add_argument("filename", type = str)
  parser.add_argument("--target_file", type = str, default = None)
  parser.add_argument("--start", type = int, default = -1)
  parser.add_argument("--end", type = int, default = 0)


  args = parser.parse_args()

  output = generate_completion_file(file = args.filename, start = args.start, end = args.end, associated_filename = args.target_file)





