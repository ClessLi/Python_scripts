from updateXml import Xml as uxml

file = 'test.xml'
with open(file, 'r+') as fp:
    config = uxml(fp, fp)
    config.read_config()
    print(config.config.)