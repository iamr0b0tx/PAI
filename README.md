# Artificially Intelligent Python (PAI)
PAI is an English to Python interprter. It is supposed to be adaptive and dynamic. It is trained in a supervised manner (look at the training file to see what it looks like).

## Contents
- ### Main.py
  This file is the main entry of the interpreter. You can run your .pai code as follows:
    ```
    python main.py program_path_name.pai
    ```

- ### Main.pai
  This is a sample file that contains a code written in english (as trained in the standard library). The contents of the file are:
  ```
  x = 3
  add x and 2
  y is add product of 7 and x and 5
  display y
  ```

- ### Main.cmd
  This is a main batch script you can use to test the program. It contains commands to automatically run the main.pai script with the main.py 
  
- ### pai.std.lib
  This is the PAI standard library, it contains the trained model of the PAI interpreter
