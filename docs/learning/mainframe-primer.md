# Mainframe primer

Just enough mainframe vocabulary to read CardDemo, and what each piece becomes in
the LegacyLens graph.

| Mainframe thing | What it is | In CardDemo | Graph node / edge |
|---|---|---|---|
| COBOL program | A source file with four divisions: IDENTIFICATION, ENVIRONMENT, DATA, PROCEDURE | `app/cbl/CBTRN02C.cbl` | `Program` |
| Paragraph | A named block of code in the PROCEDURE DIVISION, run with `PERFORM` | `1500-B-LOOKUP-ACCT` | `Paragraph`, `PERFORMS` |
| Copybook | Shared source pulled in with `COPY`, usually a record layout | `app/cpy/CVACT01Y.cpy` (account record) | `Copybook`, `INCLUDES` |
| `CALL` | A batch program calling another, like a function call | `CBSTM03A` calls `CBSTM03B` | `CALLS` |
| CICS | The transaction server that runs online screens | all `CO*` programs | |
| `EXEC CICS XCTL` | Hand control to another online program, without returning | sign-on goes to the menu | `XCTL` |
| Transaction ID | A four-character code a user types to start a program | `CC00` starts `COSGN00C` | `Transaction`, `STARTS` |
| BMS map | A 3270 screen layout | `app/bms/COSGN00.bms` | `Screen`, `USES_SCREEN` |
| JCL job | A batch script listing steps; each step runs a program | `app/jcl/POSTTRAN.jcl` | `Job`, `RUNS` |
| DD statement | Connects a file name in the program to a real dataset | `//ACCTFILE DD DSN=...ACCTDATA.VSAM.KSDS` | `READS` / `WRITES` |
| VSAM KSDS | A keyed file, much like a table with a primary key | `ACCTDATA`, `CARDXREF` | `Dataset` |
| GDG | A numbered series of versions of one file | `DALYREJS(+1)` | `Dataset` with `props.gdg` |

## How a program finds its files

A program never names a real dataset. It says `SELECT ACCOUNT-FILE ASSIGN TO ACCTFILE`.
The JCL step that runs it then says `//ACCTFILE DD DSN=AWS.M2.CARDDEMO.ACCTDATA.VSAM.KSDS`.
The parser has to join the two through the DD name, which is why reads and writes come
from both the COBOL and the JCL.

Online programs are different. They name a CICS file directly, as in
`EXEC CICS READ DATASET('USRSEC')`, sometimes through a variable.

## How to read CBTRN02C in five minutes

1. Read the comment header for its purpose.
2. Read `FILE-CONTROL` for the files it uses.
3. Read the `COPY` lines for the record layouts it shares.
4. Skim the paragraph names in the PROCEDURE DIVISION, which read like a table of
   contents.
5. Search for `MOVE 1nn TO WS-VALIDATION-FAIL-REASON` to find its business rules.

That is also what the parser automates.
