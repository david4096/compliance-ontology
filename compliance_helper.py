"""
Compliance Ontology Helper

Python utilities for working with the compliance ontology.
Provides functions to create, query, and manage compliance attestations.
"""

from rdflib import Graph, Namespace, Literal, URIRef, RDF, RDFS, OWL, XSD
from rdflib.namespace import DCTERMS
from datetime import datetime, date
from typing import Optional, List, Dict, Any
from enum import Enum


class ComplianceStatus(Enum):
    """Compliance status enumeration"""
    COMPLIANT = "Compliant"
    IN_PROGRESS = "InProgress"
    NON_COMPLIANT = "NonCompliant"
    PARTIALLY_COMPLIANT = "PartiallyCompliant"


class AttestationType(Enum):
    """Attestation type enumeration"""
    SELF_ATTESTED = "SelfAttested"
    THIRD_PARTY_ATTESTED = "ThirdPartyAttested"
    CERTIFIED_COMPLIANT = "CertifiedCompliant"
    AUDITOR_VERIFIED = "AuditorVerified"


class ComplianceFrameworkID(Enum):
    """Known compliance frameworks"""
    # US Frameworks
    ISO27001 = "ISO27001"
    CMMC = "CMMC"
    FEDRAMP = "FedRAMP"
    HIPAA = "HIPAA"
    PCI_DSS = "PCIDSS"
    GDPR = "GDPR"
    NIST_CSF = "NIST_CSF"
    NIST_800_171 = "NIST_800_171"
    NIST_800_53 = "NIST_800_53"
    ISO42001 = "ISO42001"
    SOC2 = "SOC2"

    # International Frameworks
    AU_ISM = "AU_ISM"  # Australia
    UK_CYBER_ESSENTIALS = "UK_CyberEssentials"  # United Kingdom
    CA_PIPEDA = "CA_PIPEDA"  # Canada
    SG_PDPA = "SG_PDPA"  # Singapore
    SG_MAS_TRM = "SG_MAS_TRM"  # Singapore
    JP_APPI = "JP_APPI"  # Japan
    KR_PIPA = "KR_PIPA"  # South Korea
    KR_ISMS_P = "KR_ISMS_P"  # South Korea
    IN_DPDPA = "IN_DPDPA"  # India
    BR_LGPD = "BR_LGPD"  # Brazil
    ES_ENS = "ES_ENS"  # Spain
    DE_BSI_GRUNDSCHUTZ = "DE_BSI_Grundschutz"  # Germany
    NZ_NZISM = "NZ_NZISM"  # New Zealand
    AE_IAR = "AE_IAR"  # UAE
    SA_ECC = "SA_ECC"  # Saudi Arabia
    FR_SECNUMCLOUD = "FR_SecNumCloud"  # France
    CN_MLPS = "CN_MLPS"  # China
    CN_PIPL = "CN_PIPL"  # China


class ComplianceOntology:
    """
    Main class for working with the compliance ontology.
    """

    def __init__(self, ontology_path: str = "compliance-ontology.ttl"):
        """
        Initialize the compliance ontology.

        Args:
            ontology_path: Path to the ontology TTL file
        """
        self.graph = Graph()
        self.graph.parse(ontology_path, format="turtle")

        # Define namespace
        self.ns = Namespace("http://example.org/compliance#")
        self.graph.bind("compliance", self.ns)
        self.graph.bind("dcterms", DCTERMS)

    def create_system(self,
                     system_id: str,
                     name: str,
                     description: Optional[str] = None) -> URIRef:
        """
        Create a new system in the ontology.

        Args:
            system_id: Unique identifier for the system
            name: Name of the system
            description: Optional description

        Returns:
            URIRef of the created system
        """
        system_uri = self.ns[system_id]

        self.graph.add((system_uri, RDF.type, self.ns.System))
        self.graph.add((system_uri, self.ns.systemName, Literal(name, datatype=XSD.string)))

        if description:
            self.graph.add((system_uri, self.ns.systemDescription,
                          Literal(description, datatype=XSD.string)))

        return system_uri

    def create_attester(self,
                       attester_id: str,
                       name: str,
                       credentials: Optional[str] = None) -> URIRef:
        """
        Create an attester entity.

        Args:
            attester_id: Unique identifier for the attester
            name: Name of the attester
            credentials: Optional credentials/certifications

        Returns:
            URIRef of the created attester
        """
        attester_uri = self.ns[attester_id]

        self.graph.add((attester_uri, RDF.type, self.ns.Attester))
        self.graph.add((attester_uri, self.ns.attesterName, Literal(name, datatype=XSD.string)))

        if credentials:
            self.graph.add((attester_uri, self.ns.attesterCredentials,
                          Literal(credentials, datatype=XSD.string)))

        return attester_uri

    def create_attestation(self,
                          attestation_id: str,
                          system_id: str,
                          framework: ComplianceFrameworkID,
                          status: ComplianceStatus,
                          attestation_type: AttestationType,
                          attester_id: str,
                          attestation_date: Optional[datetime] = None,
                          expiration_date: Optional[date] = None,
                          evidence: Optional[str] = None,
                          baseline: Optional[str] = None,
                          framework_version: Optional[str] = None) -> URIRef:
        """
        Create a compliance attestation.

        Args:
            attestation_id: Unique identifier for the attestation
            system_id: ID of the system being attested
            framework: Compliance framework being attested to
            status: Compliance status
            attestation_type: Type of attestation
            attester_id: ID of the attester
            attestation_date: Date of attestation (defaults to now)
            expiration_date: Optional expiration date
            evidence: Optional supporting evidence
            baseline: Optional baseline (e.g., "Low", "Moderate", "High" for FedRAMP)
            framework_version: Optional version of the framework being attested to

        Returns:
            URIRef of the created attestation
        """
        attestation_uri = self.ns[attestation_id]
        system_uri = self.ns[system_id]
        framework_uri = self.ns[framework.value]
        status_uri = self.ns[status.value]
        type_uri = self.ns[attestation_type.value]
        attester_uri = self.ns[attester_id]

        # Create attestation
        self.graph.add((attestation_uri, RDF.type, self.ns.Attestation))
        self.graph.add((system_uri, self.ns.hasAttestation, attestation_uri))
        self.graph.add((attestation_uri, self.ns.attestsCompliance, framework_uri))
        self.graph.add((attestation_uri, self.ns.hasComplianceStatus, status_uri))
        self.graph.add((attestation_uri, self.ns.hasAttestationType, type_uri))
        self.graph.add((attestation_uri, self.ns.attestedBy, attester_uri))

        # Add attestation date
        if attestation_date is None:
            attestation_date = datetime.now()
        self.graph.add((attestation_uri, self.ns.attestationDate,
                       Literal(attestation_date, datatype=XSD.dateTime)))

        # Add optional properties
        if expiration_date:
            self.graph.add((attestation_uri, self.ns.expirationDate,
                          Literal(expiration_date, datatype=XSD.date)))

        if evidence:
            self.graph.add((attestation_uri, self.ns.attestationEvidence,
                          Literal(evidence, datatype=XSD.string)))

        if framework_version:
            self.graph.add((attestation_uri, self.ns.attestedFrameworkVersion,
                          Literal(framework_version, datatype=XSD.string)))

        # If baseline specified, link to it
        if baseline:
            baseline_uri = self.ns[f"{framework.value}{baseline}"]
            self.graph.add((attestation_uri, self.ns.attestsCompliance, baseline_uri))

        return attestation_uri

    def get_system_attestations(self, system_id: str) -> List[Dict[str, Any]]:
        """
        Get all attestations for a system.

        Args:
            system_id: ID of the system

        Returns:
            List of attestation dictionaries
        """
        system_uri = self.ns[system_id]
        attestations = []

        query = f"""
        PREFIX : <http://example.org/compliance#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

        SELECT ?attestation ?framework ?status ?type ?attester ?date ?expiration ?evidence
        WHERE {{
            :{system_id} :hasAttestation ?attestation .
            ?attestation :attestsCompliance ?framework .
            ?attestation :hasComplianceStatus ?status .
            ?attestation :hasAttestationType ?type .
            ?attestation :attestedBy ?attester .
            ?attestation :attestationDate ?date .
            OPTIONAL {{ ?attestation :expirationDate ?expiration }}
            OPTIONAL {{ ?attestation :attestationEvidence ?evidence }}
        }}
        """

        results = self.graph.query(query)

        for row in results:
            attestations.append({
                'attestation': str(row.attestation),
                'framework': str(row.framework),
                'status': str(row.status),
                'type': str(row.type),
                'attester': str(row.attester),
                'date': str(row.date),
                'expiration': str(row.expiration) if row.expiration else None,
                'evidence': str(row.evidence) if row.evidence else None
            })

        return attestations

    def get_framework_info(self, framework: ComplianceFrameworkID) -> Dict[str, Any]:
        """
        Get information about a compliance framework.

        Args:
            framework: The framework to query

        Returns:
            Dictionary with framework information
        """
        framework_uri = self.ns[framework.value]

        query = f"""
        PREFIX : <http://example.org/compliance#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT ?label ?comment ?version ?url ?pubDate
        WHERE {{
            :{framework.value} rdfs:label ?label .
            OPTIONAL {{ :{framework.value} rdfs:comment ?comment }}
            OPTIONAL {{ :{framework.value} :frameworkVersion ?version }}
            OPTIONAL {{ :{framework.value} :documentationURL ?url }}
            OPTIONAL {{ :{framework.value} :publicationDate ?pubDate }}
        }}
        """

        results = self.graph.query(query)

        for row in results:
            return {
                'label': str(row.label),
                'comment': str(row.comment) if row.comment else None,
                'version': str(row.version) if row.version else None,
                'documentation_url': str(row.url) if row.url else None,
                'publication_date': str(row.pubDate) if row.pubDate else None
            }

        return {}

    def get_all_frameworks(self) -> List[Dict[str, Any]]:
        """
        Get all compliance frameworks defined in the ontology.

        Returns:
            List of framework dictionaries
        """
        query = """
        PREFIX : <http://example.org/compliance#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT ?framework ?label ?version ?url
        WHERE {
            ?framework a :ComplianceFramework .
            ?framework rdfs:label ?label .
            OPTIONAL { ?framework :frameworkVersion ?version }
            OPTIONAL { ?framework :documentationURL ?url }
        }
        ORDER BY ?label
        """

        results = self.graph.query(query)
        frameworks = []

        for row in results:
            frameworks.append({
                'uri': str(row.framework),
                'label': str(row.label),
                'version': str(row.version) if row.version else None,
                'documentation_url': str(row.url) if row.url else None
            })

        return frameworks

    def query_systems_by_compliance(self,
                                   framework: ComplianceFrameworkID,
                                   status: Optional[ComplianceStatus] = None) -> List[Dict[str, Any]]:
        """
        Query systems by their compliance status with a framework.

        Args:
            framework: The framework to check
            status: Optional status filter

        Returns:
            List of system dictionaries with compliance info
        """
        status_filter = f"?attestation :hasComplianceStatus :{status.value} ." if status else ""

        query = f"""
        PREFIX : <http://example.org/compliance#>

        SELECT ?system ?systemName ?status ?type ?date
        WHERE {{
            ?system a :System .
            ?system :systemName ?systemName .
            ?system :hasAttestation ?attestation .
            ?attestation :attestsCompliance :{framework.value} .
            ?attestation :hasComplianceStatus ?status .
            ?attestation :hasAttestationType ?type .
            ?attestation :attestationDate ?date .
            {status_filter}
        }}
        ORDER BY ?systemName
        """

        results = self.graph.query(query)
        systems = []

        for row in results:
            systems.append({
                'system': str(row.system),
                'name': str(row.systemName),
                'status': str(row.status),
                'type': str(row.type),
                'date': str(row.date)
            })

        return systems

    def save(self, output_path: str, format: str = "turtle"):
        """
        Save the ontology graph to a file.

        Args:
            output_path: Path to save the file
            format: RDF serialization format (turtle, xml, n3, etc.)
        """
        self.graph.serialize(destination=output_path, format=format)

    def validate_attestation_expiry(self, attestation_id: str) -> bool:
        """
        Check if an attestation has expired.

        Args:
            attestation_id: ID of the attestation

        Returns:
            True if expired, False if still valid or no expiration date
        """
        attestation_uri = self.ns[attestation_id]

        for _, _, exp_date in self.graph.triples((attestation_uri, self.ns.expirationDate, None)):
            expiration = datetime.fromisoformat(str(exp_date)).date()
            return date.today() > expiration

        return False


def create_example_attestations():
    """
    Create example attestations to demonstrate usage.
    """
    ontology = ComplianceOntology()

    # Create a system
    ontology.create_system(
        system_id="CloudApp1",
        name="Cloud Application Platform",
        description="Multi-tenant SaaS platform for enterprise customers"
    )

    # Create attesters
    ontology.create_attester(
        attester_id="SecurityTeam",
        name="Internal Security Team",
        credentials="CISSP, CISM certified"
    )

    ontology.create_attester(
        attester_id="ExternalAuditor",
        name="Third-Party Audit Firm",
        credentials="Authorized FedRAMP 3PAO"
    )

    # Create attestations
    ontology.create_attestation(
        attestation_id="attestation_001",
        system_id="CloudApp1",
        framework=ComplianceFrameworkID.SOC2,
        status=ComplianceStatus.COMPLIANT,
        attestation_type=AttestationType.AUDITOR_VERIFIED,
        attester_id="ExternalAuditor",
        expiration_date=date(2026, 12, 31),
        evidence="SOC 2 Type II Report available"
    )

    ontology.create_attestation(
        attestation_id="attestation_002",
        system_id="CloudApp1",
        framework=ComplianceFrameworkID.FEDRAMP,
        status=ComplianceStatus.IN_PROGRESS,
        attestation_type=AttestationType.SELF_ATTESTED,
        attester_id="SecurityTeam",
        baseline="Moderate",
        evidence="Currently in process, 80% controls implemented"
    )

    ontology.create_attestation(
        attestation_id="attestation_003",
        system_id="CloudApp1",
        framework=ComplianceFrameworkID.ISO27001,
        status=ComplianceStatus.COMPLIANT,
        attestation_type=AttestationType.CERTIFIED_COMPLIANT,
        attester_id="ExternalAuditor",
        expiration_date=date(2026, 6, 30),
        evidence="ISO 27001:2022 certificate issued"
    )

    # Save the updated ontology
    ontology.save("compliance-ontology-with-examples.ttl")

    # Query and print examples
    print("=== All Frameworks ===")
    for fw in ontology.get_all_frameworks():
        print(f"{fw['label']} v{fw['version']}")
        print(f"  URL: {fw['documentation_url']}\n")

    print("\n=== CloudApp1 Attestations ===")
    for att in ontology.get_system_attestations("CloudApp1"):
        print(f"Framework: {att['framework']}")
        print(f"Status: {att['status']}")
        print(f"Type: {att['type']}")
        print(f"Date: {att['date']}")
        if att['evidence']:
            print(f"Evidence: {att['evidence']}")
        print()


if __name__ == "__main__":
    create_example_attestations()
