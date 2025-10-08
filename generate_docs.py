#!/usr/bin/env python3
"""
Generate HTML documentation from the compliance ontology.

This script uses pyLODE to generate schema.org-style documentation
with individual pages for each term in the ontology.
"""

import subprocess
import sys
from pathlib import Path


def generate_docs():
    """Generate documentation from the ontology TTL file."""

    # Paths
    ontology_file = Path("compliance-ontology.ttl")
    docs_dir = Path("docs")

    # Ensure docs directory exists
    docs_dir.mkdir(exist_ok=True)

    # Generate main documentation page
    print("Generating ontology documentation...")

    cmd = [
        "pylode",
        str(ontology_file),
        "-o", str(docs_dir / "index.html"),
        "-c", "true",  # Include CSS
        "-s",  # Sort subjects
        "-p", "ontpub"  # Ontology publication profile
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Error generating documentation: {result.stderr}", file=sys.stderr)
        sys.exit(1)

    print(f"✓ Generated {docs_dir / 'index.html'}")

    # Create a simple README for the docs
    readme_content = """# Compliance Ontology Documentation

This documentation is automatically generated from the compliance ontology using [pyLODE](https://github.com/RDFLib/pyLODE).

## View Documentation

Visit the [main ontology documentation](index.html) to explore:
- All compliance frameworks (30+ international standards)
- Classes and properties
- Attestation types and compliance statuses
- Usage examples

## Ontology Namespace

The ontology namespace is: `http://example.org/compliance#`

## Source

The source ontology is maintained at: [compliance-ontology.ttl](../compliance-ontology.ttl)

This documentation is regenerated automatically on every push to the main branch.
"""

    (docs_dir / "README.md").write_text(readme_content)
    print(f"✓ Generated {docs_dir / 'README.md'}")

    print("\nDocumentation generation complete!")
    print(f"Open {docs_dir / 'index.html'} in a browser to view.")


if __name__ == "__main__":
    generate_docs()
