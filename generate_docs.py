#!/usr/bin/env python3
"""
Generate HTML documentation from the compliance ontology.

This script uses pyLODE to generate schema.org-style documentation
with individual pages for each term in the ontology.
"""

import subprocess
import sys
from pathlib import Path
from rdflib import Graph, Namespace, RDF, RDFS


def create_frameworks_page(docs_dir: Path):
    """Create an HTML page listing all compliance frameworks."""

    # Load ontology
    g = Graph()
    g.parse("compliance-ontology.ttl", format="turtle")
    ns = Namespace("http://example.org/compliance#")

    # Query for all frameworks
    query = """
    PREFIX : <http://example.org/compliance#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?framework ?label ?comment ?version ?url ?date
    WHERE {
        ?framework a :ComplianceFramework .
        ?framework rdfs:label ?label .
        OPTIONAL { ?framework rdfs:comment ?comment }
        OPTIONAL { ?framework :frameworkVersion ?version }
        OPTIONAL { ?framework :documentationURL ?url }
        OPTIONAL { ?framework :publicationDate ?date }
    }
    ORDER BY ?label
    """

    results = list(g.query(query))

    # Build HTML
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Compliance Frameworks - Compliance Ontology</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 1200px;
            margin: 50px auto;
            padding: 20px;
            line-height: 1.6;
        }
        h1 {
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }
        h2 {
            color: #34495e;
            margin-top: 30px;
        }
        .framework {
            margin: 20px 0;
            padding: 20px;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            background: #f9f9f9;
        }
        .framework h3 {
            margin-top: 0;
            color: #2980b9;
        }
        .framework-meta {
            color: #666;
            font-size: 0.9em;
        }
        .framework-iri {
            font-family: monospace;
            background: #ecf0f1;
            padding: 5px 10px;
            border-radius: 4px;
            margin: 10px 0;
            font-size: 0.85em;
        }
        .back-link {
            margin-bottom: 20px;
        }
        a {
            color: #3498db;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        .doc-link {
            display: inline-block;
            margin-top: 10px;
            padding: 8px 15px;
            background: #3498db;
            color: white;
            border-radius: 5px;
            text-decoration: none;
        }
        .doc-link:hover {
            background: #2980b9;
            text-decoration: none;
        }
        .count {
            color: #7f8c8d;
            font-size: 1.2em;
        }
    </style>
</head>
<body>
    <div class="back-link">
        <a href="index.html">← Back to main documentation</a> |
        <a href="downloads.html">Download formats</a>
    </div>

    <h1>Compliance Frameworks</h1>
    <p class="count">Total frameworks: <strong>""" + str(len(results)) + """</strong></p>
    <p>This ontology includes compliance and security frameworks from around the world.</p>
"""

    # Group by region
    us_intl = []
    asia_pacific = []
    europe = []
    middle_east = []
    americas = []

    for row in results:
        label = str(row.label)
        framework_data = {
            'iri': str(row.framework),
            'label': label,
            'comment': str(row.comment) if row.comment else '',
            'version': str(row.version) if row.version else 'N/A',
            'url': str(row.url) if row.url else '',
            'date': str(row.date) if row.date else ''
        }

        # Categorize
        if any(x in label for x in ['ISO', 'NIST', 'FedRAMP', 'CMMC', 'HIPAA', 'PCI DSS', 'SOC 2', 'GDPR']):
            us_intl.append(framework_data)
        elif any(x in label for x in ['Australia', 'Singapore', 'Japan', 'Korea', 'India', 'China', 'New Zealand']):
            asia_pacific.append(framework_data)
        elif any(x in label for x in ['UK', 'Spain', 'BSI', 'SecNumCloud']):
            europe.append(framework_data)
        elif any(x in label for x in ['UAE', 'Saudi']):
            middle_east.append(framework_data)
        elif any(x in label for x in ['PIPEDA', 'Brazil']):
            americas.append(framework_data)

    def render_section(title, frameworks):
        if not frameworks:
            return ""
        html = f'<h2>{title}</h2>\n'
        for fw in frameworks:
            html += f'''
    <div class="framework">
        <h3>{fw['label']}</h3>
        <div class="framework-iri"><strong>IRI:</strong> <code>{fw['iri']}</code></div>
        <p>{fw['comment']}</p>
        <div class="framework-meta">
            <strong>Version:</strong> {fw['version']}<br>
'''
            if fw['date']:
                html += f"            <strong>Published:</strong> {fw['date']}<br>\n"
            if fw['url']:
                html += f'            <a href="{fw["url"]}" class="doc-link" target="_blank">📄 Official Documentation</a>\n'
            html += '        </div>\n    </div>\n'
        return html

    html += render_section("🌐 United States & International Standards", us_intl)
    html += render_section("🌏 Asia-Pacific", asia_pacific)
    html += render_section("🇪🇺 Europe", europe)
    html += render_section("🕌 Middle East", middle_east)
    html += render_section("🌎 Americas", americas)

    html += """
    <div class="back-link" style="margin-top: 40px;">
        <a href="index.html">← Back to main documentation</a>
    </div>
</body>
</html>
"""

    frameworks_page = docs_dir / "frameworks.html"
    frameworks_page.write_text(html)
    print(f"✓ Generated frameworks listing: {frameworks_page}")


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

    # Create frameworks listing page
    create_frameworks_page(docs_dir)

    # Create a simple README for the docs
    readme_content = """# Compliance Ontology Documentation

This documentation is automatically generated from the compliance ontology using [pyLODE](https://github.com/RDFLib/pyLODE).

## View Documentation

- **[Main ontology documentation](index.html)** - Classes and properties
- **[All 30 frameworks](frameworks.html)** - Complete framework list with links
- **[Download formats](downloads.html)** - Get the ontology in various formats

## Ontology Namespace

The ontology namespace is: `http://example.org/compliance#`

## Source

The source ontology is maintained at: [compliance-ontology.ttl](../compliance-ontology.ttl)

This documentation is regenerated automatically on every push to the main branch.
"""

    (docs_dir / "README.md").write_text(readme_content)
    print(f"✓ Generated {docs_dir / 'README.md'}")

    # Run format conversion
    print("\nConverting ontology to multiple formats...")
    from convert_formats import convert_ontology
    convert_ontology()

    print("\nDocumentation generation complete!")
    print(f"Open {docs_dir / 'index.html'} in a browser to view.")
    print(f"Format downloads available at {docs_dir / 'downloads.html'}")


if __name__ == "__main__":
    generate_docs()
