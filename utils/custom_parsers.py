import json
from rest_framework import parsers
from rest_framework_xml.parsers import XMLParser


class NestedMultipartParser(parsers.MultiPartParser):
    """
    Parser for processing nested field values as well as multipart files.
    """

    def decode(self, key, value, data):

        if "[" in key and "]" in key:

            index_left_bracket = key.index("[")
            index_right_bracket = key.index("]")

            parent_key = key[:index_left_bracket]
            child_key = key[index_left_bracket + 1 : index_right_bracket]

            if parent_key not in data:
                data[parent_key] = {} if len(child_key) > 0 else []

            if "][" in key:  # if has child
                key = (
                    child_key + key[index_right_bracket + 1 :]
                )  # root[parent][child] > parent[name3]
                self.decode(key=key, value=value, data=data[parent_key])
            elif isinstance(data[parent_key], list):
                data[parent_key].append(value)
            else:
                data[parent_key][child_key] = value

        if type(value) == str:

            if ("{" in value and "}" in value) or (
                "[" in value and "]" in value
            ):
                try:
                    data[key] = json.loads(value)
                except ValueError:
                    data[key] = value
            else:
                data[key] = value

        else:
            data[key] = value

    def parse(self, stream, media_type=None, parser_context=None):
        result = super().parse(
            stream=stream, media_type=media_type, parser_context=parser_context
        )
        data = {}
        for key, value in result.data.items():
            self.decode(key=key, value=value, data=data)

        for key, value in result.files.items():
            self.decode(key=key, value=value, data=data)

        return data


# 6405 -> test merchat reference
class CustomTextXmlPaser(XMLParser):
    media_type= "text/xml"
    content_type ='text/xml'

