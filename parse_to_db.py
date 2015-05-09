from collections import OrderedDict

def convert_csv_to_graph():
    name = "\"AS Level Connectivity in Africa\""
    description = "\"Visualizing peering relationships between ASes in Africa\""
    numNodes = "1022"
    numLinks = "2531"
    numPaths = "0"
    numPathLinks = "0"
    asn_set = set([])
    asn_id_map = OrderedDict()
    with open("AS_list.csv") as f:
        for line in f:
            asn_set.add(line.strip())
    asn_list = sorted(asn_set)

    for id, asn in enumerate(asn_list):
        asn_id_map[asn] = str(id)

    source_destination_list = []

    with open("AS_connections_AF.csv") as f:
        for line in f:
            source, destination = line.strip().split(',')
            source_destination_list.append((asn_id_map[source], asn_id_map[destination]))

    # non_tree_asn = []
    # for asn in asn_list:
    # for pair in source_destination_list:

    print "Graph\n{"
    print "   ### metadata ###"
    print "   @name=" + name + ";"
    print "   @description=" + description + ";"
    print "   @numNodes=" + numNodes + ";"
    print "   @numLinks=" + numLinks + ";"
    print "   @numPaths=" + numPaths + ";"
    print "   @numPathLinks=" + numPathLinks + ";"
    print "\n"
    print "   ### structural data ###"
    print "   @links=["
    tree_link_ids = []
    unique_nodes = set([])
    for link_id, pair in enumerate(sorted(source_destination_list, key=lambda r: r[0])):
        if (pair[0] not in unique_nodes) or (pair[1] not in unique_nodes):
            unique_nodes.add(pair[0])
            unique_nodes.add(pair[1])
            tree_link_ids.append(str(link_id))
        print " { @source=" + pair[0] + "; @destination=" + pair[1] + "; },"
    print "   ];"
    print "   @paths=;"
    print "\n"
    print "   ### attribute data ###"
    print "   @enumerations=;"
    print "   @attributeDefinitions=["
    print "      {"
    print "         @name=$root;"
    print "         @type=bool;"
    print "         @default=|| false ||;"
    print "         @nodeValues=[ { @id=" + "1277" + "; @value=T; } ];"
    print "         @linkValues=;"
    print "         @pathValues=;"
    print "      },"
    print "      {"
    print "         @name=$tree_link;"
    print "         @type=bool;"
    print "         @default=|| false ||;"
    print "         @nodeValues=;"
    print "         @linkValues=["
    for link_id in tree_link_ids:
        print "            { @id=" + link_id + "; @value=T; },"
    print "         ];"
    print "         @pathValues=;"
    print "      }"
    print "   ];"
    print "   @qualifiers=["
    print "      {"
    print "         @type=$spanning_tree;"
    print "         @name=$sample_spanning_tree;"
    print "         @description=;"
    print "         @attributes=["
    print "            { @attribute=0; @alias=$root; },"
    print "            { @attribute=1; @alias=$tree_link; }"
    print "         ];"
    print "      }"
    print "  ];"
    print "\n"
    print "   ### visualization hints ###"
    print "   @filters=;"
    print "   @selectors=;"
    print "   @displays=;"
    print "   @presentations=;"
    print "\n"
    print "   ### interface hints ###"
    print "   @presentationMenus=;"
    print "   @displayMenus=;"
    print "   @selectorMenus=;"
    print "   @filterMenus=;"
    print "   @attributeMenus=;"
    print "}"
    print len(asn_list)
    print len(source_destination_list)
    print len(tree_link_ids)
    print len(unique_nodes)


def create_matrix_country(connections_file):
    '''labels	A	B	C
    A	10	15	20
    D	15	20	25
    E	20	30	50
    '''
    countries = set([])
    adj_matrix = {}
    with open(connections_file) as f:
        for line in f:
            peer1, peer2, country1, country2 = line.strip().split(',')
            if country1 not in countries:
                countries.add(country1)
            #if country2 not in countries:
            #    countries.add(country2)
            # if country1 + ',' + country2 not in adj_matrix:
            # adj_matrix[country1 + ',' + country2] = 1
            # else:
            #     adj_matrix[country1 + ',' + country2] += 1
            if country1 not in adj_matrix:
                adj_matrix[country1] = {}
            if country2 not in adj_matrix[country1]:
                adj_matrix[country1][country2] = 1
            else:
                adj_matrix[country1][country2] += 1

    print "data\t" + '\t'.join(countries)
    for c1 in sorted(countries):
        row = []
        for c2 in sorted(countries):
            if c2 in adj_matrix[c1]:
                row.append(str(adj_matrix[c1][c2]))
            else:
                row.append("-")
        print c1 + '\t' + '\t'.join(row)

def create_matrix_isn(connections_file):
    '''labels	A	B	C
    A	10	15	20
    D	15	20	25
    E	20	30	50
    '''
    isn = set([])
    adj_matrix = {}
    as_isn_map = {}
    with open('as_isn_map.csv') as f:
        for line in f:
            id, name = line.strip().replace('-', '_').split(',', 1)
            if name == '':
                as_isn_map[id] = "NULL"
            else:
                as_isn_map[id] = name

    with open(connections_file) as f:
        for line in f:
            peer1, peer2, country1, country2 = line.strip().split(',')
            if peer1 not in as_isn_map:
                isn1 = "Unidentified"
            else:
                isn1 = as_isn_map[peer1]
            if peer2 not in as_isn_map:
                isn2 = "Unidentified"
            else:
                isn2 = as_isn_map[peer2]
            if isn1 not in isn:
                isn.add(isn1)
            if isn2 not in isn:
                isn.add(isn2)

            if isn1 not in adj_matrix:
                adj_matrix[isn1] = {}
            if isn2 not in adj_matrix[isn1]:
                adj_matrix[isn1][isn2] = 1
            else:
                adj_matrix[isn1][isn2] += 1

    print "data\t" + '\t'.join(isn)

    for c1 in adj_matrix:
        row = []
        for c2 in adj_matrix:
            if c2 in adj_matrix[c1]:
                row.append(str(adj_matrix[c1][c2]))
            else:
                row.append("-")
        print c1 + '\t' + '\t'.join(row)

def create_odf(input_file):
    print "g 0 s 1 none"
    print "f 0 none length"
    print "g 1 d 1 AS Path"
    print "f 1 Frequency of Segment"
    unique_as = set([])
    unique_links = set([])
    as_map = OrderedDict()
    link_map = OrderedDict()
    as_name_map = OrderedDict()
    with open('as_map.csv') as f:
        for line in f:
            id, name = line.strip().split(',')
            if name == '':
                as_name_map[id] = "NULL"
            else:
                as_name_map[id] = name

    with open(input_file) as f:
        for line in f:
            source, destination = line.strip().split(',')
            unique_as.add(source)
            unique_as.add(destination)
            unique_links.add(source + " " + destination)

    print "t " + str(len(unique_as))
    print "T " + str(len(unique_links))
    for i, asn in enumerate(unique_as):
        as_map[asn] = str(i)

    for k, v in as_map.items():
        if k not in as_name_map:
            print "? " + v + ' ' + "not identified"
        else:
            print "? " + v + ' ' + as_name_map[k]

    for i, link in enumerate(unique_links):
        link_map[link] = str(i)

    for k, v in as_map.items():
        print "V 1 " + v

    for k, v in link_map.items():
        source, destination = k.split(' ')
        print "L " + v + ' ' + as_map[source] + ' ' + as_map[destination]

def translate_as_to_isn(csv_file):
    as_isn_map = {}
    with open('as_isn_map.csv') as f:
        for line in f:
            id, name = line.strip().replace('-', '_').split(',', 1)
            if name == '':
                as_isn_map[id] = "NULL"
            else:
                as_isn_map[id] = name

    with open(csv_file) as f:
        for line in f:
            as1, as2 = line.strip().split(',')
            if as1 not in as_isn_map:
                isn1 = "Other"
            else:
                isn1 = as_isn_map[as1]
            if as2 not in as_isn_map:
                isn2 = "Other"
            else:
                isn2 = as_isn_map[as2]
            print isn1 + ',' + isn2

#create_matrix_isn("AS_connections_with_country_AF.csv")
#create_odf("AS_connections_ZA.csv")
#translate_as_to_isn("AS_connections_SA.csv")
create_matrix_country("AS_connections_with_country_SA.csv")
# c = set([])
# d = {u'AR,SA:BO,SA': [446, 20], u'AR,SA:SR,SA': [2, 0], u'EC,SA:PE,SA': [230, 2], u'BR,SA:PE,SA': [347, 85], u'UY,SA:PY,SA': [0, 163], u'UY,SA:UY,SA': [0, 7015], u'BR,SA:CO,SA': [3789, 91], u'AR,SA:None,None': [1, 0], u'BR,SA:GF,SA': [6, 0], u'EC,SA:UY,SA': [107, 4], u'UY,SA:CO,SA': [0, 3080], u'UY,SA:CL,SA': [12, 959], u'EC,SA:EU,EU': [9, 0], u'BR,SA:AR,SA': [3506, 790], u'UY,SA:AR,SA': [4, 3411], u'BR,SA:PY,SA': [158, 49], u'UY,SA:EC,SA': [2, 1133], u'EC,SA:AR,SA': [2141, 110], u'BR,SA:IT,EU': [1, 0], u'BR,SA:UY,SA': [84, 125], u'UY,SA:PE,SA': [0, 352], u'UY,SA:GF,SA': [0, 5], u'AR,SA:GF,SA': [6, 0], u'EC,SA:BO,SA': [233, 0], u'BR,SA:SR,SA': [2, 0], u'AR,SA:US,NA': [19, 0], u'EC,SA:PY,SA': [109, 0], u'AR,SA:VE,SA': [1046, 44], u'BR,SA:EC,SA': [1372, 59], u'AR,SA:GY,SA': [14, 0], u'EC,SA:CO,SA': [1957, 91], u'AR,SA:EC,SA': [1342, 164], u'EC,SA:GY,SA': [7, 0], u'AR,SA:AR,SA': [856, 3631], u'AR,SA:PE,SA': [343, 121], u'AR,SA:UY,SA': [77, 146], u'AR,SA:CL,SA': [696, 558], u'AR,SA:BR,SA': [4841, 8893], u'BR,SA:BR,SA': [2075, 10996], u'EC,SA:US,NA': [13, 0], u'EC,SA:VE,SA': [519, 26], u'BR,SA:BO,SA': [428, 8], u'EC,SA:BR,SA': [6663, 223], u'BR,SA:US,NA': [19, 0], u'EC,SA:SR,SA': [1, 0], u'UY,SA:VE,SA': [0, 824], u'UY,SA:BR,SA': [6, 10335], u'BR,SA:None,None': [1, 0], u'UY,SA:SR,SA': [0, 2], u'UY,SA:GY,SA': [0, 9], u'EC,SA:GF,SA': [3, 0], u'EC,SA:EC,SA': [37, 713], u'UY,SA:BO,SA': [0, 347], u'AR,SA:PY,SA': [94, 124], u'EC,SA:CL,SA': [581, 44], u'AR,SA:CO,SA': [3666, 429], u'BR,SA:VE,SA': [999, 35], u'BR,SA:CL,SA': [582, 604], u'BR,SA:GY,SA': [14, 0]}
# for k in d:
#     l1 = k.split(':')[0].split(',')[0]
#     l2 = k.split(':')[1].split(',')[0]
#     c.add(l1)
#     c.add(l2)
# print sorted(c)