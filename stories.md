# Career stories

The single source of truth for career facts: roles, skills, accomplishments, education, and decisions about what never to claim. Resumes are built from this file, and this file is the one place to check for confidential or inappropriate content. Every entry is public: no identifying details (name, address, email, phone), no background, and no nonpublic system details, internal metrics, or client identities. Accomplishments use SOAR form (Situation, Objective, Action, Result).

## Target

Quality Engineer, Software Engineer in Test, or QA lead roles, especially in trading and financial data systems.

## Working approach

Tests the whole system as a black box, end to end, the way a client experiences it. Defines expected behavior with trading desks, product, engineering, and business teams before writing tests, then designs and builds the frameworks and tools that verify it.

## Never claim (all resumes)

- A lead title for roles without one; show leadership through actions
- FIX expertise; FIX is working knowledge from testing
- Current Java (last used 2007 to 2008), AWS, UI automation (last used 2007 to 2008), or recent CI configuration (last at Bank of America)
- Bash or shell scripting as a recent skill (mostly ISE and Bank of America)
- Agile as a skill
- Release readiness as a recent strength
- Speed claims for the BTCA test framework
- Other metrics beyond those stated here

## Bloomberg L.P. | Quality Engineer | Princeton, NJ | Aug 2018 to Aug 2026

Context: Bloomberg Transaction Cost Analysis (BTCA), a post-trade analytics service. Tested the instruments BTCA supports, through the end-to-end and OTC frameworks: equities; government, corporate, municipal, and mortgage bonds; FX spot, forwards, and swaps; exchange-traded index, commodity, bond, and currency derivatives (outrights, rolls, and options); and OTC interest rate, equity, and credit default swaps and options. Single-leg and multi-leg trades. Worked in two week sprints.

Skills and tools: Python | Python Behave | SQL | C++ code analysis | Linux | Windows 11 | Docker | Git | Jira | GitHub Copilot | Claude | FIX message analysis | test planning | test design | data driven testing | exploratory and regression testing | root cause analysis

### End-to-end testing for BTCA external trade feeds

- Situation: BTCA external trade feeds had no consistent testing.
- Objective: Improve the reliability of external trade feeds.
- Action: Built a no code, data driven Python framework on Windows; each test is a data file plus a validation entry, and no programming is needed to add one. It injects simulated trades and validates results by querying the BTCA Data Access API, which it used only to request data. Tested features, fixes for reported bugs, reproductions of production bugs, and requests from the publicly named Post-Trade Implementation team, which owns client onboarding and client problems. Tested end to end, from simulated feed input to final report, across BTCA and upstream systems, in daily regression against beta code. Diagnosed defects from reports, logs, FIX messages, and databases, and requested fixes from the owning teams. Copilot assisted with the API integration code and unit tests.
- Result: Consistent end-to-end validation where none existed. Supported thousands of transactions daily. As the only tester working this way, acted as test lead in practice: set the test approach, sourced test data, and automated validation. Findings could stop a release from reaching production.
- Core message: Established reliable testing for external trade feeds and owned it.
- Fits: QA lead, test automation, trading or financial data platforms
- Never claim: Speed of the framework; that the API was used to send data; that others used the framework

### Post deployment database checks

- Situation: Database transactions in a large C++ codebase lacked matching integrity checks.
- Objective: Detect data problems after each deployment.
- Action: Used Claude to scan the codebase for unchecked transactions and derive SQL checks. Reviewed and added them to the check library.
- Result: Post deployment checks executed in beta and production and were still in use at departure.
- Core message: Applied AI tooling to close gaps in production data checks.
- Fits: QA, data quality, AI assisted engineering
- Never claim: That the checks caught defects

### OTC instrument testing with Python Behave

- Situation: Clients create customized OTC instruments that BTCA must accept.
- Objective: Improve confidence that BTCA accepts those instruments.
- Action: Maintained and expanded an existing Python Behave framework for exploratory and regression testing on Linux. Wrote shell scripts connecting it to automated test execution. Containerized it with Docker; designed the Dockerfiles, which Copilot generated.
- Result: Greater confidence in BTCA support for client instruments.
- Core message: Behavior Driven Development applied to complex instruments.
- Fits: BDD, test automation, OTC instruments
- Never claim: That the framework was originally built from scratch

## Bank of America Merrill Lynch | Vice President, Quality Assurance Professional | New York, NY | May 2016 to Mar 2018

Context: Markets, Equity Derivatives. Signed off on production releases for Central Risk Book and Smart Order Router. Tested a Java-based options system as a black box.

Skills and tools: Robot Framework | FIX | TeamCity | Maven | shell scripting | test environment maintenance | release sign off

### Central Risk Book launch

- Situation: Central Risk Book was a new equity derivatives product.
- Objective: Take it from development to launch with confidence.
- Action: Designed and automated FIX message tests with Robot Framework. Analyzed custom FIX tags for integration with common infrastructure.
- Result: Tested from development to launch; signed off on its production releases.
- Core message: Owned testing of a new trading product through launch.
- Fits: Trading systems, FIX connectivity, release sign off

### Smart Order Router regression and releases

- Situation: The Smart Order Router was gaining new equity options strategies.
- Objective: Keep releases safe as coverage grew.
- Action: Expanded the Robot Framework regression suite to the new strategies. Maintained test and development environments and TeamCity pipelines, including Maven builds.
- Result: Signed off on production releases.
- Core message: Regression ownership and release sign off for order routing.
- Fits: Order routing, CI, release management

## International Securities Exchange / Nasdaq | Test Automation Engineer, System Test | New York, NY | Jul 2008 to May 2016

Context: ISE was owned by Deutsche Börse during this role. Nasdaq announced its acquisition of ISE on 2016-03-09 and completed it on 2016-06-30 (Nasdaq SEC filings); still at ISE after the announcement.

Skills and tools: .NET | C# | Python | shell scripting | fuzz testing | test framework design | QA process design

### Matching engine stress testing

- Situation: Matching engine crash defects needed to be found before production.
- Objective: Expose failures under abnormal input.
- Action: Extended a Python fuzz tool and stress tested the engine to failure, capturing core dumps for diagnosis.
- Result: Exposed defects that crashed the matching engine.
- Core message: Resilience testing of an exchange matching engine.
- Fits: Exchanges, matching engines, resilience and performance testing

### Simulated market makers for client onboarding

- Situation: Member firms needed realistic markets in the client onboarding test environment.
- Objective: Make test markets behave like production.
- Action: Contributed simulated Primary Market Makers (PMMs), one part of a larger environment built by others. PMMs control the order book and quotes for their securities, and these quoted from real market data.
- Result: Member firms tested against realistic markets.
- Core message: Built realism into client onboarding testing.
- Fits: Client onboarding, exchanges, test environments
- Never claim: Building the whole environment

### .NET automation framework and System Test process

- Situation: Trading and market data applications needed repeatable end-to-end testing and a formal test process.
- Objective: Automate testing and standardize how failures were handled.
- Action: Led development of a .NET automation framework and trained System Test engineers on it. Designed the formal System Test process. Automated failure analysis and defect disposition in a .NET results framework.
- Result: A trained team on a shared framework with automated failure analysis.
- Core message: Led framework development and defined the test process.
- Fits: Test architecture, QA process, team enablement

## DoubleClick / Google | Lead QA Automation Engineer | New York, NY | May 2007 to May 2008

Context: Worked in formal Scrum with scrum masters. Responsible for release readiness.

Skills and tools: Java | Jython | JMeter | FitNesse | JDBC | HttpUnit | HtmlUnit | Marathon | Solaris 10 | Windows Server 2003 | RHEL | MS SQL Server 2005 | Oracle 10g | load testing | UI automation

### DART Enterprise release quality

- Situation: DART Enterprise ad server releases needed fewer defects at high scale.
- Objective: Deliver a high quality release.
- Action: Led an international team of six consultants designing and executing tests. Built system test environments across three operating systems and two databases. Modeled production-like ad targeting data and load tested the server at over 1 billion impressions per day with JMeter. Deployed FitNesse for functional and database testing and Marathon for the Java GUI.
- Result: The release with the fewest defects in the product's history.
- Core message: Team leadership with a measurable quality result.
- Fits: QA leadership, performance and load testing

## NYSE | Lead Design Analyst / Programmer Analyst | New York, NY | 1999 to 2006

Context: Exact months not remembered; years only.

Skills and tools: Java | test framework design | integration testing

### Trading floor integration test framework

- Situation: Integration testing across trading floor applications was manually coordinated.
- Objective: Automate integration testing across the applications.
- Action: Built a test framework with a common scripting language to interact with each application. Learned Java here and used it for test automation of TradeWorks, a public NYSE trading floor system since retired.
- Result: Replaced manually coordinated integration testing.
- Core message: Automated integration testing for trading floor systems.
- Fits: Trading systems, test frameworks, integration testing

## Education

- M.S., Computer and Information Science, New Jersey Institute of Technology, Newark, NJ
- B.A., Applied Mathematics, William Paterson University, Wayne, NJ
