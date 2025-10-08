# Contributing to Compliance Ontology

Thank you for your interest in contributing to the Compliance Ontology project!

## Adding New Frameworks

To add a new compliance framework:

1. **Research the framework**:
   - Find official documentation URL
   - Identify current version
   - Note publication date
   - Verify enforcement authority

2. **Add to the ontology** (`compliance-ontology.ttl`):
   ```turtle
   :FrameworkID rdf:type owl:NamedIndividual ,
       :ComplianceFramework ;
       rdfs:label "Framework Name" ;
       rdfs:comment "Description of the framework" ;
       :frameworkVersion "Version Number" ;
       :documentationURL "https://official.url"^^xsd:anyURI ;
       :publicationDate "YYYY-MM-DD"^^xsd:date .
   ```

3. **Update Python helper** (`compliance_helper.py`):
   - Add framework to `ComplianceFrameworkID` enum
   - Example: `NEW_FRAMEWORK = "FrameworkID"`

4. **Test locally**:
   ```bash
   uv run python compliance_helper.py
   uv run python generate_docs.py
   open docs/index.html
   ```

5. **Submit PR**:
   - Include links to official documentation
   - Update README if adding a new country/region
   - Ensure ontology is valid Turtle syntax

## Improving Documentation

The documentation is auto-generated from the ontology, so:
- Improve descriptions in the TTL file using `rdfs:comment`
- Add more metadata properties as needed
- Documentation regenerates automatically on merge

## Code Style

- Python: Follow PEP 8
- Turtle: Use consistent indentation (4 spaces)
- Comments: Explain "why", not "what"

## Testing

Before submitting:
```bash
# Test ontology parsing
uv run python -c "from rdflib import Graph; g = Graph(); g.parse('compliance-ontology.ttl', format='turtle'); print(f'✓ Valid: {len(g)} triples')"

# Generate docs
uv run python generate_docs.py

# Run example
uv run python compliance_helper.py
```

## Questions?

Open an issue on GitHub with:
- Clear description of the framework/change
- Links to official documentation
- Why it should be included

Thank you! 🙏
