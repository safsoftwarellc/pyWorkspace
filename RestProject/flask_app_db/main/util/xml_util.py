

def get_namespace(full_xml_text):
    if full_xml_text.startswith('{'):
        return full_xml_text[1:full_xml_text.find('}')]
    return full_xml_text

def remove_namespace(full_xml_text):
    if full_xml_text.startswith('{'):
        return full_xml_text[full_xml_text.find('}')+1:]
    return full_xml_text


all_nodes={}

def get_xpath_for_element(ele, xpath_string):
    if len(list(ele))>0:
        xpath_string = xpath_string + '/' + remove_namespace(ele.tag)
        for ele1 in list(ele):
            get_xpath_for_element(ele1, xpath_string)
    else:
        if remove_namespace(ele.tag) not in all_nodes:
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

