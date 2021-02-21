import json
from jsonpath_ng.ext import parse


def replace_ref_properties_with_referenced_object(sub_dictionary, sub_dict_property, dictionary):
    """

    :param sub_dictionary:
    :param sub_dict_property:
    :param dictionary:
    :return:
    """
    references = [match.value for match in parse("$..'$ref'").find(sub_dictionary[sub_dict_property])]
    references_paths = [match.full_path for match in parse("$..'$ref'").find(sub_dictionary[sub_dict_property])]

    for i, reference in enumerate(references):

        # Getting the referenced object
        referenced_dict_path = reference.split('/')[1:]
        referenced = dictionary
        for path_elem in referenced_dict_path:
            referenced = referenced[path_elem]

        # Getting the reference parent path
        if len(references_paths) == 1:
            sub_dictionary[sub_dict_property] = referenced
        else:
            is_root = False
            reference_dict_path = []
            while not is_root:
                try:
                    references_paths[i] = references_paths[i].left
                    reference_dict_path.append(str(references_paths[i].right))
                except Exception:
                    reference_dict_path.append(str(references_paths[i]))
                    is_root = True
            reference_dict_path.reverse()
            reference_parent_key = reference_dict_path.pop()

            # Replacing the reference with the referenced object
            reference_grandparent = sub_dictionary[sub_dict_property]
            for path_elem in reference_dict_path:
                reference_grandparent = reference_grandparent[path_elem]
            reference_grandparent[reference_parent_key] = referenced


def get_response_schema(schema_name, method, status):
    """

    :param schema_name:
    :param method:
    :param status:
    :return:
    """
    api_spec = json.load(open('challenge_swagger.json'))
    replace_ref_properties_with_referenced_object(
        api_spec['paths'][schema_name][method]['responses'][status]['content']['*/*'],
        'schema',
        api_spec
    )

    return api_spec['paths'][schema_name][method]['responses'][status]['content']['*/*']['schema']
