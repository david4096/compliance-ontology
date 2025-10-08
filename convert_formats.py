#!/usr/bin/env python3
"""
Convert the compliance ontology to various OWL/RDF formats.

Supports: Turtle (TTL), RDF/XML, JSON-LD, N-Triples, N3, TriG
"""

from rdflib import Graph
from pathlib import Path
import sys


def convert_ontology(input_file: str = "compliance-ontology.ttl", output_dir: str = "docs"):
    """
    Convert the ontology to multiple RDF serialization formats.

    Args:
        input_file: Path to the input Turtle file
        output_dir: Directory to write converted files
    """

    # Create output directory if it doesn't exist
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    # Load the ontology
    print(f"Loading ontology from {input_file}...")
    g = Graph()
    g.parse(input_file, format="turtle")

    print(f"Loaded {len(g)} triples")

    # Define output formats
    formats = {
        "rdf": {
            "format": "xml",
            "extension": "rdf",
            "name": "RDF/XML",
            "description": "W3C standard XML serialization"
        },
        "jsonld": {
            "format": "json-ld",
            "extension": "jsonld",
            "name": "JSON-LD",
            "description": "JSON-based linked data format"
        },
        "nt": {
            "format": "nt",
            "extension": "nt",
            "name": "N-Triples",
            "description": "Line-based plain text format"
        },
        "n3": {
            "format": "n3",
            "extension": "n3",
            "name": "Notation3",
            "description": "Turtle superset with additional features"
        },
        "trig": {
            "format": "trig",
            "extension": "trig",
            "name": "TriG",
            "description": "Turtle extended for named graphs"
        }
    }

    # Convert to each format
    for key, fmt in formats.items():
        output_file = output_path / f"compliance-ontology.{fmt['extension']}"
        print(f"Converting to {fmt['name']}...")

        try:
            g.serialize(destination=str(output_file), format=fmt['format'])
            file_size = output_file.stat().st_size / 1024  # KB
            print(f"  ✓ Written to {output_file} ({file_size:.1f} KB)")
        except Exception as e:
            print(f"  ✗ Error: {e}", file=sys.stderr)

    # Also copy the original Turtle file
    import shutil
    turtle_dest = output_path / "compliance-ontology.ttl"
    shutil.copy2(input_file, turtle_dest)
    print(f"  ✓ Copied original Turtle to {turtle_dest}")

    # Create a downloads page
    create_downloads_page(output_path, formats)

    print("\n✅ Conversion complete!")


def create_downloads_page(output_path: Path, formats: dict):
    """Create a simple HTML page listing all download formats."""

    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Compliance Ontology - Downloads</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 900px;
            margin: 50px auto;
            padding: 20px;
            line-height: 1.6;
        }
        h1 {
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }
        .format-section {
            margin: 30px 0;
            padding: 20px;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            background: #f9f9f9;
        }
        .format-section h2 {
            margin-top: 0;
            color: #34495e;
        }
        .download-btn {
            display: inline-block;
            padding: 10px 20px;
            background: #3498db;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            margin-right: 10px;
            font-weight: bold;
        }
        .download-btn:hover {
            background: #2980b9;
        }
        .description {
            color: #666;
            margin: 10px 0;
        }
        .back-link {
            margin-top: 30px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #3498db;
            color: white;
        }
        tr:hover {
            background-color: #f5f5f5;
        }
    </style>
</head>
<body>
    <h1>Compliance Ontology Downloads</h1>

    <p>Download the compliance ontology in various RDF serialization formats. All formats contain the same semantic information, just in different syntaxes.</p>

    <table>
        <thead>
            <tr>
                <th>Format</th>
                <th>Description</th>
                <th>Download</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Turtle (TTL)</strong></td>
                <td>Terse RDF Triple Language - Human-readable, concise syntax (recommended)</td>
                <td><a href="compliance-ontology.ttl" class="download-btn">Download TTL</a></td>
            </tr>"""

    for key, fmt in formats.items():
        html += f"""
            <tr>
                <td><strong>{fmt['name']}</strong></td>
                <td>{fmt['description']}</td>
                <td><a href="compliance-ontology.{fmt['extension']}" class="download-btn">Download {fmt['extension'].upper()}</a></td>
            </tr>"""

    html += """
        </tbody>
    </table>

    <div class="format-section">
        <h2>📖 What's the difference?</h2>
        <ul>
            <li><strong>Turtle (.ttl)</strong> - Most human-readable, recommended for editing and version control</li>
            <li><strong>RDF/XML (.rdf)</strong> - W3C standard, widely supported by tools</li>
            <li><strong>JSON-LD (.jsonld)</strong> - Best for web applications and APIs</li>
            <li><strong>N-Triples (.nt)</strong> - Simple line-based format, easy to parse programmatically</li>
            <li><strong>Notation3 (.n3)</strong> - Turtle superset with additional features</li>
            <li><strong>TriG (.trig)</strong> - Turtle extended for named graphs and datasets</li>
        </ul>
    </div>

    <div class="format-section">
        <h2>🔗 Ontology Information</h2>
        <ul>
            <li><strong>Namespace:</strong> <code>http://example.org/compliance#</code></li>
            <li><strong>Version:</strong> 1.0.0</li>
            <li><strong>Frameworks:</strong> 30 international compliance frameworks</li>
            <li><strong>GitHub:</strong> <a href="https://github.com/david4096/compliance-ontology">david4096/compliance-ontology</a></li>
        </ul>
    </div>

    <p class="back-link">
        <a href="index.html">← Back to ontology documentation</a>
    </p>
</body>
</html>
"""

    downloads_page = output_path / "downloads.html"
    downloads_page.write_text(html)
    print(f"  ✓ Created downloads page: {downloads_page}")


if __name__ == "__main__":
    convert_ontology()
