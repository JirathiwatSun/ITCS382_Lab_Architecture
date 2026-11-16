#!/usr/bin/env python3
"""Build a PDF of all ITCS382 Architecture Lab quiz answers."""

from pathlib import Path

from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    Image,
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
)

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "submission" / "ITCS382_Architecture_Lab_Answers.pdf"
DIAG = ROOT / "submission" / "diagrams"


def styles():
    base = getSampleStyleSheet()
    s = {
        "title": ParagraphStyle(
            "TitleCustom",
            parent=base["Title"],
            fontSize=16,
            leading=20,
            spaceAfter=6,
            alignment=TA_CENTER,
        ),
        "subtitle": ParagraphStyle(
            "SubtitleCustom",
            parent=base["Normal"],
            fontSize=10,
            leading=13,
            spaceAfter=14,
            alignment=TA_CENTER,
            textColor="#333333",
        ),
        "h1": ParagraphStyle(
            "H1Custom",
            parent=base["Heading1"],
            fontSize=13,
            leading=16,
            spaceBefore=14,
            spaceAfter=8,
            textColor="#111111",
        ),
        "h2": ParagraphStyle(
            "H2Custom",
            parent=base["Heading2"],
            fontSize=11,
            leading=14,
            spaceBefore=10,
            spaceAfter=4,
            textColor="#1a1a1a",
        ),
        "body": ParagraphStyle(
            "BodyCustom",
            parent=base["Normal"],
            fontSize=9.5,
            leading=12.5,
            spaceAfter=6,
            alignment=TA_JUSTIFY,
        ),
        "code": ParagraphStyle(
            "CodeCustom",
            parent=base["Code"],
            fontName="Courier",
            fontSize=7.5,
            leading=9.5,
            leftIndent=4,
            spaceBefore=4,
            spaceAfter=8,
            backColor="#f5f5f5",
        ),
        "caption": ParagraphStyle(
            "CaptionCustom",
            parent=base["Normal"],
            fontSize=8.5,
            leading=11,
            spaceBefore=2,
            spaceAfter=10,
            alignment=TA_CENTER,
            textColor="#444444",
        ),
        "meta": ParagraphStyle(
            "MetaCustom",
            parent=base["Normal"],
            fontSize=9,
            leading=12,
            spaceAfter=4,
            alignment=TA_LEFT,
        ),
    }
    return s


def P(text, style):
    return Paragraph(text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"), style)


def add_image(story, path, caption, s, max_w=16 * cm, max_h=10 * cm):
    if not path.exists():
        story.append(P(f"[Missing image: {path.name}]", s["caption"]))
        return
    img = Image(str(path))
    w, h = img.imageWidth, img.imageHeight
    scale = min(max_w / w, max_h / h, 1.0)
    img.drawWidth = w * scale
    img.drawHeight = h * scale
    story.append(KeepTogether([img, P(caption, s["caption"])]))


def build():
    s = styles()
    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=A4,
        leftMargin=1.6 * cm,
        rightMargin=1.6 * cm,
        topMargin=1.4 * cm,
        bottomMargin=1.4 * cm,
        title="ITCS382 Architecture Lab Answers",
        author="JirathiwatSun",
    )
    story = []

    story.append(P("ITCS382 Software Design and Modeling", s["title"]))
    story.append(P("Lab: Intended and Implemented Architecture — Quiz Answers", s["title"]))
    story.append(
        P(
            "Team qwerty · Phase 2 repo ICT-Mahidol/2026-ITCS382-Sec1-Gemini8 (commit bd2d68c) · "
            "Answers prepared 15–16 November 2026 · JDK 25 / jdeps 25.0.5 / Maven 3.10.0",
            s["subtitle"],
        )
    )
    story.append(
        P(
            "Submit by pasting each quiz question into MyCourses. This PDF is a complete backup of "
            "questions 1–11 plus the AI declaration, with Mermaid diagrams rendered from jdeps.",
            s["body"],
        )
    )

    # ---------- Q1 ----------
    story.append(P("Quiz Question 1 — Part A (questions 1–4)", s["h1"]))
    story.append(P("1. Why jdeps reads target/classes, and what it prints before mvn package", s["h2"]))
    story.append(
        P(
            "jdeps analyses bytecode, not source code. In a .class file the compiler has already "
            "resolved every type that a class uses into a fully qualified name, such as "
            "parcelpoint.service.ParcelService, so jdeps can read the real dependencies directly. "
            "In a .java file this information is incomplete: classes in the same package need no "
            "import, imports can use wildcards (import parcelpoint.domain.*), and a class can be "
            "written with its fully qualified name in the code without any import. Only compiling "
            "resolves all of these, so mvn package must run first to create target/classes. If I "
            "run jdeps before mvn package (I tested this after mvn clean), it prints only "
            '"Warning: Path does not exist: target/classes" and no dependency lines. It still '
            "exits with code 0, so an empty result means nothing was checked, not that there are "
            "no dependencies.",
            s["body"],
        )
    )

    story.append(P("2. Why domain→domain and storage→storage do not count", s["h2"]))
    story.append(
        P(
            "These lines mean that a class uses another class in the same package. For example, "
            "Parcel uses ParcelSize and ParcelStatus, and H2ParcelRepository implements "
            "ParcelRepository. That is collaboration inside one package (its cohesion), not "
            "coupling between two packages. The package diagram only draws arrows between different "
            "packages, so a line from a package to itself can neither match nor break any arrow of "
            "the design. (cli and service have no such line only because each holds a single class.)",
            s["body"],
        )
    )

    story.append(P("3. Does implemented match intended?", s["h2"]))
    story.append(
        P(
            "Yes, the implemented architecture matches the intended architecture exactly. I "
            "compared them in both directions. From code to diagram, each of the 8 jdeps arrows "
            "(parcelpoint→cli, parcelpoint→service, parcelpoint→storage, cli→domain, cli→service, "
            "service→domain, service→storage, storage→domain) is in the package diagram. From "
            "diagram to code, the diagram has the same 8 arrows and each one is in the jdeps "
            "output. There is no extra arrow, no missing arrow and no cycle: every arrow points "
            "down towards domain, and domain depends on no other package.",
            s["body"],
        )
    )
    add_image(
        story,
        DIAG / "parcelpoint.png",
        "Figure 1. ParcelPoint implemented architecture (from jdeps, Step A4).",
        s,
        max_h=8 * cm,
    )

    story.append(P("4. Why Main→storage is allowed but cli→storage is forbidden", s["h2"]))
    story.append(
        P(
            "Main is the composition root. It is not part of any layer; its only job is to start "
            "the program and wire the layers together. Some class has to choose the concrete "
            "H2ParcelRepository and pass it into ParcelService as a ParcelRepository (dependency "
            "injection). Doing it in Main keeps that choice in one line in one place, and Main has "
            "no business or user-interface logic, so storage details do not leak anywhere else. "
            "cli is the presentation layer. In the layered style each layer may talk only to the "
            "layer directly below it, so cli must go through service. If cli used storage "
            "directly, it would skip the service layer, bypass its rules (locker allocation and "
            "fees), and tie the user interface to the database technology. Every change of storage "
            "would then ripple into the user interface.",
            s["body"],
        )
    )

    # ---------- Q2 ----------
    story.append(P("Quiz Question 2 — Part B (questions 5–9)", s["h1"]))
    story.append(P("5. Prediction before running", s["h2"]))
    story.append(
        P(
            "I predicted the new line parcelpoint.cli → parcelpoint.storage. After mvn package "
            "(which still showed BUILD SUCCESS) and jdeps, this was exactly the one new line.",
            s["body"],
        )
    )

    story.append(P("6. Layered-style rule broken, and file-store consequence", s["h2"]))
    story.append(
        P(
            "The change breaks the rule of the layered style that a layer may only use the layer "
            "directly below it, so no layer may be skipped. The path cli → service → storage "
            "became cli → storage directly. ParcelCommandLine now hard-codes the concrete class "
            "H2ParcelRepository and the path \"./data/parcelpoint\". If the team moved from H2 to "
            "a file store, changing Main would no longer be enough. ParcelCommandLine would also "
            "have to be edited, recompiled and retested, although nothing in the user interface "
            "changed. If someone forgot it, the staff command would keep reading the old H2 "
            "database while store and pickup used the new file store. The staff list would then "
            "show stale or wrong data, or fail completely once the H2 file was removed.",
            s["body"],
        )
    )

    story.append(P("7. Why the class view helps more", s["h2"]))
    story.append(
        P(
            "The package view only says that some class in cli uses some class in storage. The "
            "class view names both classes: parcelpoint.cli.ParcelCommandLine → "
            "parcelpoint.storage.H2ParcelRepository. It tells me exactly which file to open and "
            "which type to remove. It also separates the allowed uses (Main → H2ParcelRepository, "
            "Main → ParcelRepository and ParcelService → ParcelRepository) from the forbidden "
            "one, and it shows that the drift uses the concrete class rather than the interface. "
            "In a real project with many classes in each package, this saves searching through "
            "every file by hand.",
            s["body"],
        )
    )

    story.append(P("8. Why the domain↔storage cycle is harmful", s["h2"]))
    story.append(
        P(
            "The cycle creates tight, two-way coupling. domain depends on storage and storage "
            "depends on domain, so the two packages can no longer be understood, built or used "
            "separately and in effect become one unit. In terms of connascence, Parcel now has "
            "connascence of name and type with ParcelRepository (it knows its name and the "
            "signature of save), and ParcelRepository already had connascence of name and type "
            "with Parcel. This strong connascence now crosses the package boundary in both "
            "directions, while the guideline is to keep strong connascence inside a module and "
            "only weak connascence between modules. Change: a change to ParcelRepository.save can "
            "force a change in Parcel, and a change in Parcel can force a change in the "
            "repository, so ripples run both ways. Test: to unit-test a simple rule such as "
            "Parcel.fee, I now have to compile against, and possibly stub, the storage package. "
            "Reuse: I cannot take domain into another program, such as a web version, without "
            "also taking storage with it. It also lowers the cohesion of Parcel, which now mixes "
            "business rules with persistence.",
            s["body"],
        )
    )

    story.append(P("9. Why the compiler accepted the drifts, and why jdeps is needed", s["h2"]))
    story.append(
        P(
            "The compiler only checks that the code is valid Java: every type exists on the "
            "classpath, is accessible, and is used with the right signature. H2ParcelRepository "
            "and ParcelRepository are public classes on the same classpath, so any class in any "
            "package may use them. Java has no concept of layers. The package diagram lives in a "
            "design document that the compiler never reads, and Java's access modifiers (public "
            "or package-private) cannot express a rule like \"public, but only for service and "
            "Main\". The program also still ran correctly, so tests would not fail either. A team "
            "therefore needs a separate, automated architecture check (a fitness function) such "
            "as jdeps, run on every build or in CI. It compares the real dependencies with the "
            "allowed arrows and catches a one-line shortcut as soon as it appears, before such "
            "shortcuts pile up. This kind of change is easy to miss in code review.",
            s["body"],
        )
    )

    # ---------- Q3 ----------
    story.append(PageBreak())
    story.append(P("Quiz Question 3 — Part C (questions 10–11)", s["h1"]))
    story.append(
        P(
            "Team name: qwerty (repository ICT-Mahidol/2026-ITCS382-Sec1-Gemini8, branch master, "
            "commit bd2d68c, checked on 16 November 2026).",
            s["meta"],
        )
    )
    story.append(
        P(
            "The code implements all four selected use cases (UC01, UC07, UC09 and UC04). "
            "mvn package shows BUILD SUCCESS. The root package is ocs. The package diagram was "
            "updated (H2 and the .mv.db file are now notes, not Java packages), but the ocs.* "
            "package arrows are the same.",
            s["body"],
        )
    )

    story.append(P("10. jdeps output and Mermaid flowcharts", s["h2"]))
    story.append(P("jdeps -verbose:package -filter:none -e \"ocs.*\" target/classes", s["meta"]))
    jdeps_out = """classes -> target\\classes
   ocs.app          -> ocs.domain         classes
   ocs.app          -> ocs.port           classes
   ocs.cli          -> ocs.app            classes
   ocs.cli          -> ocs.cli            classes
   ocs.cli          -> ocs.domain         classes
   ocs.cli          -> ocs.persistence    classes
   ocs.cli          -> ocs.port           classes
   ocs.cli          -> ocs.simulation     classes
   ocs.domain       -> ocs.domain         classes
   ocs.domain       -> ocs.port           classes
   ocs.persistence  -> ocs.domain         classes
   ocs.persistence  -> ocs.persistence    classes
   ocs.persistence  -> ocs.port           classes
   ocs.port         -> ocs.domain         classes
   ocs.simulation   -> ocs.domain         classes
   ocs.simulation   -> ocs.port           classes"""
    story.append(Preformatted(jdeps_out, s["code"]))
    story.append(
        P(
            "After skipping the first line and self-lines, 13 arrows remain. Nodes drop the ocs. prefix.",
            s["body"],
        )
    )
    add_image(
        story,
        DIAG / "ocs_implemented.png",
        "Figure 2. Implemented architecture (jdeps, commit bd2d68c). Orange = missing from diagram; red = cycle cause.",
        s,
        max_h=7.5 * cm,
    )
    add_image(
        story,
        DIAG / "ocs_intended.png",
        "Figure 3. Intended architecture (internal ocs.* arrows from qwerty_D4_PackageDiagram).",
        s,
        max_h=6.5 * cm,
    )

    story.append(P("11. Differences and cycles", s["h2"]))
    story.append(
        P(
            "From code to diagram, 9 of 13 jdeps arrows are in the diagram and 4 are not. From "
            "diagram to code, all 9 diagram arrows are in jdeps. There is 1 cycle. Causing classes "
            "were found with jdeps -verbose:class.",
            s["body"],
        )
    )

    findings = [
        (
            "(a) Arrow in code, not in diagram — cli → domain",
            "Where: ScienceProgramCommandLine, StatusEnquiryCommandLine, CommandSequenceCommandLine, "
            "ObservingQueueCommandLine and OcsMain use domain types. Fix the design: services return "
            "domain objects that CLI must display; class diagram already has ScienceProgramCommandLine "
            "→ SciencePlan. Add cli → domain.",
        ),
        (
            "(b) Arrow in code, not in diagram — cli → port",
            "Where: only OcsMain uses the nine port interfaces. Fix the design: OcsMain is the "
            "composition root (same allowed case as ParcelPoint Main → storage). Add cli → port, "
            "noting only OcsMain may use it.",
        ),
        (
            "(c) Arrow in code, not in diagram — port → domain",
            "Where: every port interface uses domain value types in signatures. Fix the design: "
            "correct Ports-and-Adapters direction. Add port → domain.",
        ),
        (
            "(d) Arrow in code, not in diagram — domain → port",
            "Where: HealthMonitor, MotionCoordinator, SubsystemTelemetryMonitor. Fix the code: "
            "creates the cycle in (f); report says domain must not import adapter packages; these "
            "classes do application coordination.",
        ),
        (
            "(e) Arrow in diagram, not in code",
            "Where: none. All 9 internal diagram arrows appear in jdeps. Extra check: persistence "
            "→ java.sql; H2 is runtime-only. Diagram notes for H2/.mv.db match that.",
        ),
        (
            "(f) Cycle — domain ↔ port",
            "Fix the code: move HealthMonitor, MotionCoordinator and SubsystemTelemetryMonitor "
            "from ocs.domain to ocs.app. That removes domain → port; domain then depends on nothing. "
            "After also adding the three design arrows above, code and design match with 12 arrows "
            "and no cycle.",
        ),
    ]
    for title, body in findings:
        story.append(P(title, s["h2"]))
        story.append(P(body, s["body"]))

    # ---------- Q4 ----------
    story.append(P("Quiz Question 4 — AI usage declaration", s["h1"]))
    story.append(P("Tool: Cursor (Agent mode)", s["meta"]))
    story.append(P("Exact model: Claude Opus 5.5 (Anthropic)", s["meta"]))
    story.append(P("Date of use: 15 November 2026 and 16 November 2026", s["meta"]))
    story.append(
        P(
            "What I used it for: running the lab steps (mvn package, and the jdeps package and "
            "class views) for Parts A, B and C; drafting the explanations for questions 1 to 11; "
            "reading my team's package diagram on the latest commit (bd2d68c); comparing the "
            "intended and implemented architectures; rendering the Mermaid flowcharts as images.",
            s["body"],
        )
    )
    story.append(P("How I checked each answer:", s["meta"]))
    story.append(
        P(
            "Questions 1 to 9 (Parts A and B): I compared every jdeps line with the outputs "
            "printed in the lab sheet for Steps A2, B1, B2, B3 and B4, and they matched. I checked "
            "the answer about running jdeps before mvn package by running jdeps after mvn clean, "
            'which printed "Warning: Path does not exist: target/classes". I checked the '
            "explanations against the lecture terms: layered style, coupling, cohesion and "
            "connascence.",
            s["body"],
        )
    )
    story.append(
        P(
            "Questions 10 and 11 (Part C): On 16 November 2026 I pulled the latest team commit "
            "bd2d68c, rebuilt ocs with mvn package, and re-ran jdeps. I traced every arrow of "
            "qwerty_D4_PackageDiagram.svg by hand and compared it with the 13 jdeps arrows in "
            "both directions. For each class named by the class view, I opened the Java file and "
            "found the import, for example import ocs.port.TelescopePort; in MotionCoordinator.java. "
            "I checked that the four extra arrows and the domain/port cycle are still present on "
            "this commit.",
            s["body"],
        )
    )

    story.append(Spacer(1, 8 * mm))
    story.append(P("End of quiz answers", s["caption"]))
    doc.build(story)
    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    build()
