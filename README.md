# Whale Lang 🐋🐋🐋

### Compilords

- [Program structure](#program-structure)
- [Data Types](#data-types)
  - [Primitive types](#primitive-types)
    - [Literals](#literals)
- [Scopes](#scopes)
- [Global Space Members](#global-space-members)
  - [Global Variables](#global-variables)
  - [Functions](#functions)
- [Statements](#statements)
  - [Calling Functions](#calling-functions)
- [Control Statements](#control-statements)
  - [Condition Statement](#condition-statement)
  - [Loop Statement](#loop-statement)
- [Dimensioned variables](#dimensioned-variables)
- [Expressions](#expressions)
  - [Arithmetic Operators](#arithmetic-operators)
  - [Relational Operators](#relational-operators)
  - [Assignment Operatos](#assignment-operatos)
- [Special Functions](#special-functions)
  - [Write](#write)
  - [Read](#read)
- [Comments](#comments)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Program structure

A Compilord program starts with all the name of the program, followed by all the
declaration of the global variables, declaration of the functions and the main function

1. Global Variables Declarations
2. Functions
3. Main Function

## Data Types

### Primitive types

Compilord language allows for the following primitive types:

- Integer: positive or negative numbers, without decimals, of unlimited length.
  - Ex.: -1, 0, 1, 2, 3.
- Float: positive or negative numbers that can contain decimals.
  - Ex: -1.5, 0, 1.5, 2.0, 3.75.
- Char: stores the value of a char
  - Ex.: "a", "b", "c"

The language follows arithmetic logic: [Logical Arithmetic](#logical-arithmetic)

#### Literals

| Data Type | Representation                    | Example             |
| --------- | --------------------------------- | ------------------- |
| Integer   | Numeric value                     | 0, 1, 2, ...        |
| Float     | Numeric value with decimal points | 0, 1, 2.0, 3.5, ... |
| Char      | Single char with double quotes    | "a", "b", "C"       |

## Scopes

The Compilord language allows for both global variables and function-local variables

## Global Space Members

### Global Variables

Global variables like this:

_let data_type_;

    data_type {
      int
      float
      char
    }

You can also declare multiple variables like this:

_let data_type_ _var_name, var_name, var_name_;

Global variables can't have the same name as a local or another global variable

### Assignment

You can assign values to vars like this

_var_name_ = _expression_

        x = 10  20;

### Functions

You can declare Local Variables in functions like this:

        int function myFunc()
        let int x;
        let int y;
        {

        }

Functions can be defined like this:

_return_type_ _function_ _func_name_ (_param1_, _param2_) {
_statements_;
}

        int sumNums(int x, int y)
        {
            return x + y;
        }

Functions can return any primitive data type or void

Functions only receive primitive values, not arrays

## Statements

### Calling Functions

You can call functions like this:

_func_name_(_expressions_);

You can use non void functions as expressions like this:

       x = _func_name_(10) + 10;

However you cannot use void functions as expressions

## Control Statements

This languague take a binary approach to conditions, if the value is not 1 then it's false

### Condition Statement

Condition statements can be defined like this:

if (_condition_) {
_statements_;
} else {
_statements_;
}

### Loop Statement

While statements can be defined like this

while (_condition_) {
_statements_;
}

For statements can be defined like this

for (_var = n to m_) {
_statements_;
}

    for (x = 1 to 100) {
      write(x);
    }

## Dimensioned variables

Arrays and matrices start from 0

        arr[10]; # this goes from 0 to 9

Arrays can be declared like this:

_data_type_ _var_name_[*integer_literal*];

    int x[10];  # Array of 10 positions.

To call an array use this:

_var_name_[expression];

    a = x[3];  # Assign the value in the third position of x to a

Matrices can be declared like this:

_data_type_ _var_name_[*integer_literal*]_[*integer_literal*]_;

    int x[10][10];  # Matrix of 10 by 10.

You can access a matrix value like this

    a = x[5][6];  # access matrix in row 5 column 6.

## Expressions

### Arithmetic Operators

- Binary operators

  | Operation      | Token |
  | -------------- | ----- |
  | Addition       | +     |
  | Substraction   | -     |
  | Multiplication | \*    |
  | Division       | /     |
  | Floor Division | /.    |
  | &              | &     |
  | |              | |     |

- Unary operators

  | Operation | Token |
  | --------- | ----- |
  | Not       | !     |

### Relational Operators

- Binary operators

  | Operation          | Token |
  | ------------------ | ----- |
  | More Than          | >     |
  | Less Than          | <     |
  | More or Equal Than | >=    |
  | Less or equal Than | <=    |
  | Equal To           | ==    |
  | Not equal          | !=    |

### Assignment Operators

- Binary Operator

  | Operation | Token |
  | --------- | ----- |
  | Equal     | =     |

## Special Functions

The language provides the following special functions:

#### Write

Allows you to print elements to console:

write _expressions_;

    write(a); # prints the value of a in the console

## Comments

Use the '//' token to write comments in a single line:

    // This is a comment

Use the '/\* \*/' to multilne comment

    /* This is a comment
       this is still a comment
       this is still a comment
    */
