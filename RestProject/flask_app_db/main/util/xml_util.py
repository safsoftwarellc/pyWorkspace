

def get_namespace(full_xml_text):
    if full_xml_text.startswith('{'):
        return full_xml_text[1:full_xml_text.find('}')]
    return full_xml_text

def remove_namespace(full_xml_text):
    if full_xml_text.startswith('{'):
        return full_xml_text[full_xml_text.find('}')+1:]
    return full_xml_text



def get_xpath_for_element(ele, xpath_string, all_nodes):
    if len(list(ele))>0:
        xpath_string = xpath_string + '/' + remove_namespace(ele.tag)
        for ele1 in list(ele):
            all_nodes = get_xpath_for_element(ele1, xpath_string, all_nodes)
    else:
        all_nodes.append(xpath_string + '/' + remove_namespace(ele.tag) + ' - ' + remove_namespace(ele.tag))
        """if remove_namespace(ele.tag) not in all_nodes:
            if not ele.text:
                all_nodes[remove_namespace(ele.tag)]=xpath_string + '/' + remove_namespace(ele.tag) + '-' + remove_namespace(ele.tag) +'-None'
            else:
                all_nodes[remove_namespace(ele.tag)]=xpath_string + '/' + remove_namespace(ele.tag) + '-' + remove_namespace(ele.tag) + '-' + ele.text
        else:
            tag_name = remove_namespace(ele.tag)
            tag_name1 = remove_namespace(ele.tag)
            count = 0
            while(tag_name1 in all_nodes):
                count += 1
                tag_name1 = tag_name + '_' + str(count)
            if not ele.text:
                all_nodes[tag_name1]=xpath_string + '/' + remove_namespace(ele.tag) + '-' + remove_namespace(ele.tag) +'-None'
            else:
                all_nodes[tag_name1]=xpath_string + '/' + remove_namespace(ele.tag) + '-' + remove_namespace(ele.tag) + '-' + ele.text
        """    
    return all_nodes

def get_updated_xml(root, all_xpaths, json_data):
    ns = get_namespace_info_from_xpaths(all_xpaths)
    return replace_xml_values_by_xpath(root, all_xpaths, json_data, ns)


def replace_xml_values_by_xpath(root, all_xpaths, json_data, ns):
    
    for xpath_key in all_xpaths:
        ns_xpath_key = get_namespace_updated_xpath(xpath_key, ns)

        if all_xpaths[xpath_key] in json_data:
            xpath_value = json_data[all_xpaths[xpath_key]]
            if ns is None:
                for ele in root.xpath(ns_xpath_key):
                    ele.text = xpath_value
            else:
                for ele in root.xpath(ns_xpath_key, namespaces=ns):
                    ele.text = xpath_value
    return root
                    
def get_namespace_info_from_xpaths(all_xpaths):
    for xpath_key in all_xpaths:
        if all_xpaths[xpath_key] == 'ns':
            return {'xmlns': xpath_key}
    return None

def get_namespace_updated_xpath(xpath_string, ns):
    if ns is None:
        return xpath_string

    xpath_string_list = xpath_string.split('/')
    last_index_of_list = len(xpath_string_list)-1
    extra_slash = False
    if xpath_string_list[last_index_of_list] == '':
        extra_slash = True
        del(xpath_string_list[last_index_of_list])

    xpath_string = '/xmlns:'.join(xpath_string_list)
    if extra_slash:
        xpath_string = xpath_string + '/'
    
    return xpath_string
