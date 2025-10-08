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

| Framework | Version | Documentation |
|-----------|---------|---------------|
| ISO 27001 | 2022 | https://www.iso.org/standard/27001 |
| CMMC | 2.0 | https://dodcio.defense.gov/CMMC/ |
| FedRAMP | Rev. 5 (Low/Moderate/High) | https://www.fedramp.gov/rev5/baselines/ |
| HIPAA Security Rule | 45 CFR Part 160 & 164 | https://www.hhs.gov/hipaa/for-professionals/security/ |
| PCI DSS | 4.0.1 | https://www.pcisecuritystandards.org/document_library/ |
| GDPR | Regulation (EU) 2016/679 | https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng |
| NIST CSF | 2.0 | https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf |
| NIST SP 800-171 | Revision 3 | https://csrc.nist.gov/pubs/sp/800/171/r3/final |
| NIST SP 800-53 | Revision 5 | https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final |
| ISO 42001 | 2023 | https://www.iso.org/standard/42001 |
| SOC 2 | 2017 TSC (Revised 2022) | https://www.aicpa-cima.com/topic/audit-assurance/soc-2 |

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

- Framework properties: `frameworkVersion`, `documentationURL`, `publicationDate`
- Attestation properties: `attestationDate`, `expirationDate`, `attestationEvidence`
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

Contributions welcome! Please ensure any additions maintain OWL consistency and include appropriate documentation links for compliance frameworks.
