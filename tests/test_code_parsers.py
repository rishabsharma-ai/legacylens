"""Unit tests for the COBOL, JCL and CICS extractors, on small inline snippets."""

from pathlib import Path

from legacylens.ingest.code import cics, cobol, jcl
from legacylens.ingest.code.model import dataset_name


def fixed(*lines: str) -> str:
    """Lay out code in fixed-format columns: 6-char sequence area, indicator, code."""
    out = []
    for line in lines:
        if line.startswith("*"):
            out.append("000000" + line)
        else:
            out.append("000000 " + line)
    return "\n".join(out) + "\n"


def write(tmp_path: Path, name: str, text: str) -> Path:
    path = tmp_path / name
    path.write_text(text)
    return path


PROGRAM = fixed(
    "*****************************************************",
    "* Function    : Post the daily transactions.",
    "*****************************************************",
    "IDENTIFICATION DIVISION.",
    "PROGRAM-ID.    DEMO01C.",
    "ENVIRONMENT DIVISION.",
    "FILE-CONTROL.",
    "    SELECT ACCOUNT-FILE ASSIGN TO ACCTFILE",
    "    SELECT REJECT-FILE ASSIGN TO DALYREJS.",
    "DATA DIVISION.",
    "WORKING-STORAGE SECTION.",
    "    COPY CVACT01Y.",
    "*   COPY COMMENTED.",
    "01  WS-VARS.",
    "    05 WS-FILE       PIC X(08) VALUE 'USRSEC  '.",
    "PROCEDURE DIVISION.",
    "MAIN-PARA.",
    "    OPEN I-O ACCOUNT-FILE",
    "         OUTPUT REJECT-FILE",
    "    PERFORM 1000-CHECK THRU 1000-EXIT",
    "    CALL 'SUBPGM' USING WS-VARS",
    "    EXEC CICS XCTL",
    "         PROGRAM ('COMEN01C')",
    "    END-EXEC",
    "    EXEC CICS READ",
    "         DATASET (WS-FILE)",
    "    END-EXEC",
    "    GOBACK.",
    "1000-CHECK.",
    "    MOVE 102 TO WS-VALIDATION-FAIL-REASON",
    "    MOVE 'OVERLIMIT TRANSACTION'",
    "      TO WS-VALIDATION-FAIL-REASON-DESC",
    "    COMPUTE WS-INT",
    "       = (WS-BAL * WS-RATE) / 1200",
    "    .",
    "1000-EXIT.",
    "    EXIT.",
)


def test_program_basics(tmp_path):
    prog = cobol.parse_program(write(tmp_path, "DEMO01C.cbl", PROGRAM))
    assert prog.name == "DEMO01C"
    assert prog.summary == "Post the daily transactions."
    assert prog.kind == "online"  # it has EXEC CICS
    assert prog.copies == ["CVACT01Y"]  # the commented-out COPY is ignored
    assert prog.calls[0][0] == "SUBPGM"


def test_paragraphs_and_performs(tmp_path):
    prog = cobol.parse_program(write(tmp_path, "DEMO01C.cbl", PROGRAM))
    names = [p.name for p in prog.paragraphs]
    assert names == ["MAIN-PARA", "1000-CHECK", "1000-EXIT"]
    main = prog.paragraphs[0]
    assert [t for t, _ in main.performs] == ["1000-CHECK", "1000-EXIT"]


def test_files_and_open_modes(tmp_path):
    prog = cobol.parse_program(write(tmp_path, "DEMO01C.cbl", PROGRAM))
    assert prog.selects == {"ACCOUNT-FILE": "ACCTFILE", "REJECT-FILE": "DALYREJS"}
    assert prog.opens == {"ACCOUNT-FILE": {"READS", "WRITES"}, "REJECT-FILE": {"WRITES"}}


def test_cics_targets_resolve_through_values(tmp_path):
    prog = cobol.parse_program(write(tmp_path, "DEMO01C.cbl", PROGRAM))
    xctl = next(b for b in prog.cics if b["command"] == "XCTL")
    read = next(b for b in prog.cics if b["command"] == "READ")
    assert cobol.resolve_all(xctl["program"], prog.values, prog.moves) == ["COMEN01C"]
    assert cobol.resolve_all(read["dataset"], prog.values, prog.moves) == ["USRSEC"]


def test_business_rules(tmp_path):
    prog = cobol.parse_program(write(tmp_path, "DEMO01C.cbl", PROGRAM))
    texts = {r["text"] for r in prog.rules}
    assert "Reason 102: OVERLIMIT TRANSACTION" in texts
    assert "COMPUTE WS-INT = (WS-BAL * WS-RATE) / 1200" in texts
    assert all(r["paragraph"] == "1000-CHECK" for r in prog.rules)


def test_jcl_steps_and_dds(tmp_path):
    path = write(
        tmp_path,
        "POSTDEMO.jcl",
        "\n".join(
            [
                "//POSTDEMO JOB 'POST',CLASS=A",
                "//* a comment",
                "//STEP15 EXEC PGM=DEMO01C",
                "//STEPLIB  DD DISP=SHR,",
                "//            DSN=AWS.M2.CARDDEMO.LOADLIB",
                "//ACCTFILE DD DISP=SHR,",
                "//         DSN=AWS.M2.CARDDEMO.ACCTDATA.VSAM.KSDS",
                "//DALYREJS DD DISP=(NEW,CATLG,DELETE),",
                "//         DSN=AWS.M2.CARDDEMO.DALYREJS(+1)",
            ]
        ),
    )
    job = jcl.parse_job(path)
    assert job.name == "POSTDEMO"
    step = job.steps[0]
    assert (step.name, step.program) == ("STEP15", "DEMO01C")
    dds = {d.name: (d.dsn, d.disp) for d in step.dds}
    assert dds["ACCTFILE"] == ("AWS.M2.CARDDEMO.ACCTDATA.VSAM.KSDS", "SHR")
    assert dds["DALYREJS"] == ("AWS.M2.CARDDEMO.DALYREJS(+1)", "NEW")


def test_dataset_names():
    assert dataset_name("AWS.M2.CARDDEMO.ACCTDATA.VSAM.KSDS") == "ACCTDATA"
    assert dataset_name("AWS.M2.CARDDEMO.CARDXREF.VSAM.AIX.PATH") == "CARDXREF"
    assert dataset_name("AWS.M2.CARDDEMO.DALYREJS(+1)") == "DALYREJS"
    assert dataset_name("AWS.M2.CARDDEMO.DALYTRAN.PS") == "DALYTRAN"


def test_csd(tmp_path):
    path = write(
        tmp_path,
        "X.CSD",
        "\n".join(
            [
                " DEFINE TRANSACTION(CC00) GROUP(CARDDEMO)",
                "        PROGRAM(COSGN00C) TWASIZE(0)",
                " DEFINE FILE(ACCTDAT) GROUP(CARDDEMO)",
                "        DSNAME(AWS.M2.CARDDEMO.ACCTDATA.VSAM.KSDS) RLSACCESS(NO)",
            ]
        ),
    )
    defs = cics.parse_csd(path)
    assert defs["transactions"] == {"CC00": "COSGN00C"}
    assert defs["files"] == {"ACCTDAT": "AWS.M2.CARDDEMO.ACCTDATA.VSAM.KSDS"}


def test_ims_segments_and_mq_queues(tmp_path):
    src = cobol.Source.read(
        write(
            tmp_path,
            "MQIMS.cbl",
            fixed(
                "PROCEDURE DIVISION.",
                "    EXEC DLI GU USING PCB(1)",
                "        SEGMENT (PAUTSUM0)",
                "        INTO (SUMMARY)",
                "    END-EXEC.",
                "    EXEC DLI ISRT USING PCB(1)",
                "        SEGMENT (PAUTSUM0) SEGMENT (PAUTDTL1)",
                "    END-EXEC.",
                "    EXEC DLI SCHD PSB((PSB-NAME)) END-EXEC.",
                "    MOVE 'CARD.DEMO.ERROR' TO ERROR-QUEUE-NAME.",
                "    CALL 'MQPUT' USING HCONN.",
            ),
        )
    )
    assert cobol.dli_segments(src) == [
        ("READS", "PAUTSUM0", 2),
        ("WRITES", "PAUTSUM0", 6),
        ("WRITES", "PAUTDTL1", 6),
    ]
    assert cobol.mq_queues(src) == [("WRITES", "CARD.DEMO.ERROR", 10)]
