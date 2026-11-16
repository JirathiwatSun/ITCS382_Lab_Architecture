# ITCS382 Lab: Intended and Implemented Architecture — Quiz Answers

Commands re-checked on 16 November 2026 against team commit `bd2d68c`, with JDK 25 (`jdeps` 25.0.5) and Maven 3.10.0.
Paste-ready plain-text copies live in `submission/Q1_PartA.txt` … `Q4_AI_Declaration.txt`.

---

## Quiz Question 1 — Part A

1. jdeps analyses bytecode, not source code. In a .class file the compiler has already resolved every type that a class uses into a fully qualified name, such as parcelpoint.service.ParcelService, so jdeps can read the real dependencies directly. In a .java file this information is incomplete: classes in the same package need no import, imports can use wildcards (import parcelpoint.domain.*), and a class can be written with its fully qualified name in the code without any import. Only compiling resolves all of these, so mvn package must run first to create target/classes. If I run jdeps before mvn package (I tested this after mvn clean), it prints only "Warning: Path does not exist: target/classes" and no dependency lines. It still exits with code 0, so an empty result means nothing was checked, not that there are no dependencies.

2. These lines mean that a class uses another class in the same package. For example, Parcel uses ParcelSize and ParcelStatus, and H2ParcelRepository implements ParcelRepository. That is collaboration inside one package (its cohesion), not coupling between two packages. The package diagram only draws arrows between different packages, so a line from a package to itself can neither match nor break any arrow of the design. (cli and service have no such line only because each holds a single class.)

3. Yes, the implemented architecture matches the intended architecture exactly. I compared them in both directions. From code to diagram, each of the 8 jdeps arrows (parcelpoint->cli, parcelpoint->service, parcelpoint->storage, cli->domain, cli->service, service->domain, service->storage, storage->domain) is in the package diagram. From diagram to code, the diagram has the same 8 arrows and each one is in the jdeps output. There is no extra arrow, no missing arrow and no cycle: every arrow points down towards domain, and domain depends on no other package.

My Mermaid flowchart of the implemented architecture:
flowchart TD
    parcelpoint --> cli
    parcelpoint --> service
    parcelpoint --> storage
    cli --> domain
    cli --> service
    service --> domain
    service --> storage
    storage --> domain

4. Main is the composition root. It is not part of any layer; its only job is to start the program and wire the layers together. Some class has to choose the concrete H2ParcelRepository and pass it into ParcelService as a ParcelRepository (dependency injection). Doing it in Main keeps that choice in one line in one place, and Main has no business or user-interface logic, so storage details do not leak anywhere else. cli is the presentation layer. In the layered style each layer may talk only to the layer directly below it, so cli must go through service. If cli used storage directly, it would skip the service layer, bypass its rules (locker allocation and fees), and tie the user interface to the database technology. Every change of storage would then ripple into the user interface.


---

## Quiz Question 2 — Part B

5. I predicted the new line parcelpoint.cli -> parcelpoint.storage. After mvn package (which still showed BUILD SUCCESS) and jdeps, this was exactly the one new line.

6. The change breaks the rule of the layered style that a layer may only use the layer directly below it, so no layer may be skipped. The path cli -> service -> storage became cli -> storage directly. ParcelCommandLine now hard-codes the concrete class H2ParcelRepository and the path "./data/parcelpoint". If the team moved from H2 to a file store, changing Main would no longer be enough. ParcelCommandLine would also have to be edited, recompiled and retested, although nothing in the user interface changed. If someone forgot it, the staff command would keep reading the old H2 database while store and pickup used the new file store. The staff list would then show stale or wrong data, or fail completely once the H2 file was removed.

7. The package view only says that some class in cli uses some class in storage. The class view names both classes: parcelpoint.cli.ParcelCommandLine -> parcelpoint.storage.H2ParcelRepository. It tells me exactly which file to open and which type to remove. It also separates the allowed uses (Main -> H2ParcelRepository, Main -> ParcelRepository and ParcelService -> ParcelRepository) from the forbidden one, and it shows that the drift uses the concrete class rather than the interface. In a real project with many classes in each package, this saves searching through every file by hand.

8. The cycle creates tight, two-way coupling. domain depends on storage and storage depends on domain, so the two packages can no longer be understood, built or used separately and in effect become one unit. In terms of connascence, Parcel now has connascence of name and type with ParcelRepository (it knows its name and the signature of save), and ParcelRepository already had connascence of name and type with Parcel. This strong connascence now crosses the package boundary in both directions, while the guideline is to keep strong connascence inside a module and only weak connascence between modules.
Change: a change to ParcelRepository.save can force a change in Parcel, and a change in Parcel can force a change in the repository, so ripples run both ways.
Test: to unit-test a simple rule such as Parcel.fee, I now have to compile against, and possibly stub, the storage package.
Reuse: I cannot take domain into another program, such as a web version, without also taking storage with it.
It also lowers the cohesion of Parcel, which now mixes business rules with persistence.

9. The compiler only checks that the code is valid Java: every type exists on the classpath, is accessible, and is used with the right signature. H2ParcelRepository and ParcelRepository are public classes on the same classpath, so any class in any package may use them. Java has no concept of layers. The package diagram lives in a design document that the compiler never reads, and Java's access modifiers (public or package-private) cannot express a rule like "public, but only for service and Main". The program also still ran correctly, so tests would not fail either. A team therefore needs a separate, automated architecture check (a fitness function) such as jdeps, run on every build or in CI. It compares the real dependencies with the allowed arrows and catches a one-line shortcut as soon as it appears, before such shortcuts pile up. This kind of change is easy to miss in code review.


---

## Quiz Question 3 — Part C

Team name: qwerty (repository ICT-Mahidol/2026-ITCS382-Sec1-Gemini8, branch master, commit bd2d68c, checked on 16 November 2026)

The code implements all four selected use cases (UC01, UC07, UC09 and UC04). mvn package shows BUILD SUCCESS. The root package is ocs. The package diagram in qwerty_D4_Design.md was updated since the previous check (H2 and the .mv.db file are now drawn as notes, not Java packages), but the ocs.* package arrows are the same.

10. jdeps output of Step C2:

> jdeps -verbose:package -filter:none -e "ocs.*" target/classes
classes -> target\classes
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
   ocs.simulation   -> ocs.port           classes

After skipping the first line and the lines from a package to itself, 13 arrows remain. No class sits directly in the root package ocs (OcsMain is in ocs.cli), so every node drops the "ocs." prefix.

My Mermaid flowchart (implemented architecture):
flowchart TD
    cli --> app
    cli --> domain
    cli --> persistence
    cli --> port
    cli --> simulation
    app --> domain
    app --> port
    domain --> port
    persistence --> domain
    persistence --> port
    port --> domain
    simulation --> domain
    simulation --> port

These are the internal arrows of the intended architecture, as I read them from the team's package diagram (qwerty_D4_PackageDiagram.svg in qwerty_D4_Design.md). The external JDBC package and the H2/.mv.db notes are left out because -e "ocs.*" hides them.
flowchart TD
    cli --> app
    cli --> persistence
    cli --> simulation
    app --> domain
    app --> port
    persistence --> domain
    persistence --> port
    simulation --> domain
    simulation --> port

11. From code to diagram, 9 of the 13 jdeps arrows are in the diagram and 4 are not. From diagram to code, all 9 arrows of the diagram are in the jdeps output. There is 1 cycle. I found the class behind each arrow with the class view of Step B2 (jdeps -verbose:class -filter:none -e "ocs.port.*" target/classes, and the same with "ocs.domain.*").

(a) What I found: an arrow in the code that the diagram does not show.
Where: cli -> domain. The classes are ScienceProgramCommandLine -> SciencePlan, ObservingProgram, TargetCoordinates, InstrumentSettings and EvaluationResult; StatusEnquiryCommandLine -> StatusReport, Telemetry and QualityReport; CommandSequenceCommandLine -> ObservingSequence and SequenceState; ObservingQueueCommandLine -> QueueRecommendation; and OcsMain -> Scheduler, ResourceAllocator, ProgramValidator, HealthMonitor, MotionCoordinator and more.
What I would fix: the design. The dependency is really needed. The services return domain objects that the command lines must display, the team's own class diagram already has ScienceProgramCommandLine -> SciencePlan, and OcsMain must construct the domain services. Add the arrow cli -> domain (ParcelPoint has the same arrow).

(b) What I found: an arrow in the code that the diagram does not show.
Where: cli -> port. The only class is ocs.cli.OcsMain, which uses all nine port interfaces (ProgramRepository, QueueRepository, SequenceRepository, EventLog, SimulatorPort, ObservatoryContextPort, TelescopePort, EnclosurePort and InstrumentPort).
What I would fix: the design. OcsMain is the composition root. It wires the adapters to the services through the port types, which is exactly what the Ports and Adapters section of the report describes. This is the same allowed case as ParcelPoint's Main -> storage.ParcelRepository. None of the four command-line classes uses a port, so it is not a shortcut. Add cli -> port to the diagram, with a note that only OcsMain may use it.

(c) What I found: an arrow in the code that the diagram does not show.
Where: port -> domain. Every port interface uses domain value types in its method signatures, for example TelescopePort -> TargetCoordinates and Telemetry; InstrumentPort -> InstrumentSettings, RawData and Telemetry; ProgramRepository -> SciencePlan and ObservingProgram; SequenceRepository -> ObservingSequence, QualityReport and RawData.
What I would fix: the design. A port must describe its operations in the domain's own types, which is the correct direction in Ports and Adapters. The alternative, passing lists of primitives, would increase connascence of position. Add port -> domain to the diagram.

(d) What I found: an arrow in the code that the diagram does not show.
Where: domain -> port. The classes are HealthMonitor -> TelescopePort, EnclosurePort and InstrumentPort; MotionCoordinator -> TelescopePort and EnclosurePort; SubsystemTelemetryMonitor -> TelescopePort, EnclosurePort and InstrumentPort.
What I would fix: the code. This arrow creates the cycle described in (f), and it goes against the report's own rule that domain types do not import application or adapter packages. These three classes coordinate devices for a use case, which is application work rather than a domain rule.

(e) What I found: an arrow in the diagram that the code does not have.
Where: none. All 9 internal arrows of the diagram (cli->app, cli->persistence, cli->simulation, app->domain, app->port, persistence->domain, persistence->port, simulation->domain and simulation->port) are in the jdeps output.
What I would fix: nothing. As an extra check outside the ocs.* filter, a separate jdeps run confirms persistence -> java.sql. There is no compile-time persistence -> org.h2 dependency, because the H2 driver is loaded at runtime from the JDBC URL. The current diagram draws H2 and the .mv.db file as notes rather than Java packages, which matches that.

(f) What I found: a cycle between packages.
Where: domain <-> port. The arrow domain -> port comes from the three classes in (d), and the arrow port -> domain comes from the port signatures in (c).
What I would fix: the code. I would break the cycle by removing domain -> port: move HealthMonitor, MotionCoordinator and SubsystemTelemetryMonitor from ocs.domain to ocs.app, next to the services that use them (SequenceService and StatusService). No other domain class refers to them. After that move, domain depends on no other package and the cycle is gone. The arrows that remain (app -> port, app -> domain and port -> domain) are all allowed in the corrected diagram.

After these fixes, the diagram gains cli -> domain, cli -> port and port -> domain, and the code loses domain -> port. Code and design then match with 12 arrows and no cycle.


---

## Quiz Question 4 — AI usage declaration

Tool: Cursor (Agent mode)
Exact model: Claude Opus 5.5 (Anthropic)
Date of use: 15 November 2026 and 16 November 2026

What I used it for: running the lab steps (mvn package, and the jdeps package and class views) for Parts A, B and C; drafting the explanations for questions 1 to 11; reading my team's package diagram on the latest commit (bd2d68c); comparing the intended and implemented architectures; rendering the Mermaid flowcharts as images.

How I checked each answer:
- Questions 1 to 9 (Parts A and B): I compared every jdeps line with the outputs printed in the lab sheet for Steps A2, B1, B2, B3 and B4, and they matched. I checked the answer about running jdeps before mvn package by running jdeps after mvn clean, which printed "Warning: Path does not exist: target/classes". I checked the explanations against the lecture terms: layered style, coupling, cohesion and connascence.
- Questions 10 and 11 (Part C): On 16 November 2026 I pulled the latest team commit bd2d68c, rebuilt ocs with mvn package, and re-ran jdeps. I traced every arrow of qwerty_D4_PackageDiagram.svg by hand and compared it with the 13 jdeps arrows in both directions. For each class named by the class view, I opened the Java file and found the import, for example import ocs.port.TelescopePort; in MotionCoordinator.java. I checked that the four extra arrows and the domain/port cycle are still present on this commit.
