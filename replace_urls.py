from lxml import etree
from bs4 import BeautifulSoup as BS

ns = {"kml": "http://www.opengis.net/kml/2.2"}

# Preserve CDATA sections
parser = etree.XMLParser(remove_blank_text=True, strip_cdata=False)

tree = etree.parse("./Vaghela/doc.kml", parser=parser)

for placemark in tree.xpath("//kml:Placemark", namespaces=ns):

    # pick up the name and strip of spaces
    placemark_name = placemark.xpath("kml:name/text()", namespaces=ns)[0]
    stripped_name = placemark_name.replace(" ", "")

    # we need the object reference to replace it later
    description_old = placemark.xpath(
        "kml:description", namespaces=ns)[0]
    # xpath text() ignores cdata - which works in our favour
    # replacing src is straightforward now
    description_old_text = "".join(description_old.itertext())

    # parse with beautifulsoup and replace src attribute with new url
    soup = BS(description_old_text, features="lxml")
    soup.img[
        "src"] = f"https://raw.githubusercontent.com/DeeprajPandey/ciar/main/Vaghela/{stripped_name}.png"
    # remove the extra html//body tags from soup
    soup.html.unwrap()
    soup.body.unwrap()
    # place img tag with updated src url in CDATA tag
    updated_description_text = f"<![CDATA[{str(soup)}]]>"

    # create new description object and replace with new cdata
    description_new = etree.Element(etree.QName(
        ns.get("kml"), "description"), nsmap=ns)
    description_new.text = updated_description_text

    description_old.getparent().replace(description_old, description_new)

with open("doc_new.kml", "w") as kml_outfile:
    kml_outfile.write(etree.tostring(tree, pretty_print=True).decode("UTF-8"))


# from pykml import parser
# from pykml.factory import write_python_script_for_kml_document

# with open("./Vaghela/doc.kml") as kml_infile:
#     root = parser.parse(kml_infile).getroot()

# Generate pykml script to generate kml file
# script = write_python_script_for_kml_document(root)
# print(script)
