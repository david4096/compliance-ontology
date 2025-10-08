# Compliance Ontology

An OWL ontology for representing compliance frameworks, attestations, and compliance status for system security requirements.

## Overview

This ontology provides a structured way to represent:
- **Compliance frameworks** (ISO 27001, FedRAMP, NIST, HIPAA, PCI DSS, GDPR, SOC 2, etc.)
- **Attestations** (self-attested, third-party attested, certified, auditor-verified)
- **Compliance status** (compliant, in progress, non-compliant, partially compliant)
- **Systems** and their compliance relationships
- **Framework baselines** (e.g., FedRAMP Low/Moderate/High)

## Files

- `compliance-ontology.ttl` - The OWL ontology in Turtle format
- `compliance_helper.py` - Python utilities for working with the ontology
- `pyproject.toml` - Project configuration and dependencies

## Supported Frameworks

The ontology includes **30 compliance frameworks** covering global security and privacy requirements:

### United States & International Standards
| Framework | Version | Link |
|-----------|---------|------|
| [ISO/IEC 27001](https://www.iso.org/isoiec-27001-information-security.html) | 2022 | [Website](https://www.iso.org/isoiec-27001-information-security.html) |
| [ISO 42001 (AI)](https://www.iso.org/standard/81230.html) | 2023 | [Website](https://www.iso.org/standard/81230.html) |
| [CMMC](https://dodcio.defense.gov/CMMC/) | 2.0 | [Website](https://dodcio.defense.gov/CMMC/) |
| [FedRAMP](https://www.fedramp.gov/) | Rev. 5 (Low/Moderate/High) | [Website](https://www.fedramp.gov/) |
| [HIPAA Security Rule](https://www.hhs.gov/hipaa/) | 45 CFR Part 160 & 164 | [Website](https://www.hhs.gov/hipaa/) |
| [PCI DSS](https://www.pcisecuritystandards.org/) | 4.0.1 | [Website](https://www.pcisecuritystandards.org/) |
| [GDPR (EU)](https://gdpr.eu/) | Regulation (EU) 2016/679 | [Website](https://gdpr.eu/) |
| [NIST CSF](https://www.nist.gov/cyberframework) | 2.0 | [Website](https://www.nist.gov/cyberframework) |
| [NIST SP 800-171](https://csrc.nist.gov/projects/cprt/catalog#/cprt/framework/version/SP_800_171_3_0_0) | Revision 3 | [Website](https://csrc.nist.gov/pubs/sp/800/171/r3/final) |
| [NIST SP 800-53](https://csrc.nist.gov/projects/cprt/catalog#/cprt/framework/version/SP_800_53_5_1_1) | Revision 5 | [Website](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final) |
| [SOC 2](https://www.aicpa-cima.com/topic/audit-assurance/soc-2) | 2017 TSC (Revised 2022) | [Website](https://www.aicpa-cima.com/topic/audit-assurance/soc-2) |

### Asia-Pacific
- 🇦🇺 **Australia**: [ISM (Information Security Manual)](https://www.cyber.gov.au/)
- 🇸🇬 **Singapore**: [PDPA](https://www.pdpc.gov.sg/), [MAS TRM](https://www.mas.gov.sg/)
- 🇯🇵 **Japan**: [APPI (Personal Information Protection)](https://www.ppc.go.jp/en/)
- 🇰🇷 **South Korea**: [PIPA](https://www.pipc.go.kr/np/default/page.do?mCode=E020010000), [K-ISMS-P](https://isms.kisa.or.kr/)
- 🇮🇳 **India**: [DPDPA (Digital Personal Data Protection Act)](https://www.meity.gov.in/)
- 🇨🇳 **China**: [MLPS 2.0](https://www.gov.cn/), [PIPL](http://www.npc.gov.cn/)
- 🇳🇿 **New Zealand**: [NZISM](https://www.gcsb.govt.nz/)

### Europe
- 🇬🇧 **United Kingdom**: [Cyber Essentials & Cyber Essentials Plus](https://www.ncsc.gov.uk/cyberessentials/overview)
- 🇪🇸 **Spain**: [ENS (Esquema Nacional de Seguridad)](https://ens.ccn.cni.es/)
- 🇩🇪 **Germany**: [BSI IT-Grundschutz](https://www.bsi.bund.de/)
- 🇫🇷 **France**: [SecNumCloud (ANSSI)](https://cyber.gouv.fr/)

### Middle East
- 🇦🇪 **UAE**: [IA Regulation (NESA)](https://u.ae/)
- 🇸🇦 **Saudi Arabia**: [ECC (Essential Cybersecurity Controls)](https://nca.gov.sa/)

### Americas
- 🇨🇦 **Canada**: [PIPEDA](https://www.priv.gc.ca/)
- 🇧🇷 **Brazil**: [LGPD](https://www.gov.br/anpd/)

## Installation

Using [uv](https://github.com/astral-sh/uv):

```bash
uv sync
```

## Usage

### Basic Usage

```python
from compliance_helper import ComplianceOntology, ComplianceFrameworkID, ComplianceStatus, AttestationType
from datetime import date

# Load the ontology
ontology = ComplianceOntology("compliance-ontology.ttl")

# Create a system
ontology.create_system(
    system_id="MyApp",
    name="My Application",
    description="Production application"
)

# Create an attester
ontology.create_attester(
    attester_id="AuditFirm",
    name="Security Audit Company",
    credentials="FedRAMP 3PAO"
)

# Create an attestation
ontology.create_attestation(
    attestation_id="attestation_001",
    system_id="MyApp",
    framework=ComplianceFrameworkID.SOC2,
    status=ComplianceStatus.COMPLIANT,
    attestation_type=AttestationType.AUDITOR_VERIFIED,
    attester_id="AuditFirm",
    expiration_date=date(2026, 12, 31),
    evidence="SOC 2 Type II Report"
)

# Save changes
ontology.save("my-compliance-data.ttl")
```

### Query Framework Information

```python
# Get information about a specific framework
info = ontology.get_framework_info(ComplianceFrameworkID.NIST_CSF)
print(f"{info['label']} v{info['version']}")
print(f"Documentation: {info['documentation_url']}")

# List all frameworks
for framework in ontology.get_all_frameworks():
    print(f"{framework['label']} - {framework['version']}")
```

### Query System Attestations

```python
# Get all attestations for a system
attestations = ontology.get_system_attestations("MyApp")
for att in attestations:
    print(f"Framework: {att['framework']}")
    print(f"Status: {att['status']}")
    print(f"Type: {att['type']}")
    print(f"Date: {att['date']}")
```

### Query Systems by Compliance

```python
# Find all systems compliant with ISO 27001
systems = ontology.query_systems_by_compliance(
    framework=ComplianceFrameworkID.ISO27001,
    status=ComplianceStatus.COMPLIANT
)

for system in systems:
    print(f"{system['name']}: {system['status']}")
```

### Check Attestation Expiry

```python
# Check if an attestation has expired
is_expired = ontology.validate_attestation_expiry("attestation_001")
if is_expired:
    print("Attestation has expired and needs renewal")
```

## Ontology Structure

### Core Classes

- **System** - A system, application, or organization
- **Attestation** - A compliance attestation
- **ComplianceFramework** - A compliance or security framework
- **Baseline** - A specific baseline within a framework
- **Attester** - An entity providing attestation
- **ComplianceStatus** - Status of compliance
- **AttestationType** - Type of attestation

### Object Properties

- `hasAttestation` - Links system to attestation
- `attestsCompliance` - Links attestation to framework
- `hasComplianceStatus` - Status of attestation
- `hasAttestationType` - Type of attestation
- `attestedBy` - Entity that provided attestation
- `hasBaseline` - Links framework to baselines

### Data Properties

- Framework properties: `frameworkVersion`, `homepageURL`, `documentationURL`, `publicationDate`
- Attestation properties: `attestationDate`, `expirationDate`, `attestationEvidence`, `attestedFrameworkVersion`
- System properties: `systemName`, `systemDescription`
- Attester properties: `attesterName`, `attesterCredentials`
- Baseline properties: `baselineName`, `controlCount`

## Compliance Status Values

- **Compliant** - Fully compliant with the framework
- **InProgress** - Working towards compliance
- **NonCompliant** - Not compliant with the framework
- **PartiallyCompliant** - Partially compliant

## Attestation Types

- **SelfAttested** - Self-assessment by the organization
- **ThirdPartyAttested** - Independent third-party assessment
- **CertifiedCompliant** - Official certification
- **AuditorVerified** - Independent auditor verification

## Example

Run the included example to see the ontology in action:

```bash
uv run compliance-example
```

Or directly:

```bash
uv run python compliance_helper.py
```

This will create example attestations and demonstrate querying capabilities.

## Documentation

The ontology documentation is automatically generated and published to GitHub Pages using [pyLODE](https://github.com/RDFLib/pyLODE).

**View the documentation:** https://david4096.github.io/compliance-ontology/

Each term in the ontology has its own section with:
- IRI (namespace + term)
- Description
- Domain and range information
- Related properties

The documentation is regenerated automatically on every push to main via GitHub Actions.

### Download Formats

The ontology is available in multiple RDF serialization formats:

**[📥 Download page](https://david4096.github.io/compliance-ontology/downloads.html)** - Available formats:
- **Turtle (.ttl)** - Human-readable, recommended for editing
- **RDF/XML (.rdf)** - W3C standard XML serialization
- **JSON-LD (.jsonld)** - JSON-based linked data format
- **N-Triples (.nt)** - Simple line-based format
- **Notation3 (.n3)** - Turtle superset
- **TriG (.trig)** - Extended for named graphs

### Generating Documentation Locally

```bash
uv run python generate_docs.py
open docs/index.html
open docs/downloads.html
```

## Extending the Ontology

### Adding New Frameworks

To add a new framework, add an individual in the TTL file:

```turtle
:NewFramework rdf:type owl:NamedIndividual ,
    :ComplianceFramework ;
    rdfs:label "Framework Name" ;
    rdfs:comment "Framework description" ;
    :frameworkVersion "1.0" ;
    :documentationURL "https://example.com/docs"^^xsd:anyURI ;
    :publicationDate "2024-01-01"^^xsd:date .
```

### Adding Control-Level Attestations

The ontology is designed to be extensible to control-level attestations. Future versions could add:

```turtle
:Control rdf:type owl:Class ;
    rdfs:comment "A specific control within a framework" .

:hasControl rdf:type owl:ObjectProperty ;
    rdfs:domain :ComplianceFramework ;
    rdfs:range :Control .

:attestsControl rdf:type owl:ObjectProperty ;
    rdfs:domain :Attestation ;
    rdfs:range :Control .
```

## License

[Specify your license here]

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:
- Adding new compliance frameworks
- Improving documentation
- Testing changes

Please ensure any additions:
- Maintain OWL consistency
- Include official documentation links
- Add proper version information
- Follow existing patterns in the ontology

## Project Structure

```
compliance-ontology/
├── compliance-ontology.ttl      # Main ontology (single source of truth)
├── compliance_helper.py         # Python utilities for working with ontology
├── generate_docs.py            # Documentation generator
├── convert_formats.py          # Multi-format RDF converter
├── pyproject.toml             # uv project configuration
├── .github/workflows/docs.yml # CI/CD for GitHub Pages
└── docs/                      # Generated (not in git)
    ├── index.html            # Main documentation
    ├── downloads.html        # Format downloads page
    └── compliance-ontology.* # All RDF formats
```

## Acknowledgments

- [pyLODE](https://github.com/RDFLib/pyLODE) for ontology documentation generation
- [rdflib](https://github.com/RDFLib/rdflib) for RDF processing
- All the standards bodies and organizations maintaining the compliance frameworks
