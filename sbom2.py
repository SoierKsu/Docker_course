# Ensure GraphViz and sbom2dot are installed.
$ dot --version
$ python -m pip install sbom2dot

# Create an SVG from an SBOM!
$ sbom2dot -i bom.cdx.json | dot -Tsvg -o bom.cdx.svg

# Open the SVG, either in image viewer or browser.
$ firefox bom.cdx.svg
