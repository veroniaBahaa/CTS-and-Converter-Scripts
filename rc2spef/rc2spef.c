// rc2spef

#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <getopt.h>

#include "readliberty.h"	/* liberty file database */

#define SRC     0x01    // node is a driver
#define SNK     0x02    // node is a receiver
#define INT     0x03    // node is internal to an interconnect

typedef struct _r *rptr;
typedef struct _node *nodeptr;

typedef struct _r {
    char       *name;
    nodeptr     node1;
    nodeptr     node2;
    double      rval;
} r;

typedef struct _ritem* ritemptr;

typedef struct _ritem {
    rptr        r;
    ritemptr    next;
} ritem;


typedef struct _node {
    char*       name;
    int         type;
    ritemptr    rlist;
    double      nodeCap;
    double      totCapDownstream;
    double      totCapDownstreamLessGates;
    short       visited;
} node;

void print_node (nodeptr node) {
    printf("Name: %s\n", node->name);
    printf("Type: %d\n", node->type);
    printf("Cap: %.10f\n", node->nodeCap);
    printf("DownstreamCap: %.10f\n", node->totCapDownstream);
    printf("DownstreamCapLessGates: %.10f\n", node->totCapDownstreamLessGates);
    printf("\n");
}

typedef struct _node_item *node_item_ptr;

typedef struct _node_item {
    nodeptr         node;
    node_item_ptr   prev;
    node_item_ptr   next;
} node_item;

typedef struct _snk* snkptr;

typedef struct _snk {
    nodeptr     snknode;
    double      delay;
    snkptr      next;
} snk;

typedef struct _elmdly* elmdlyptr;

typedef struct _elmdly {
    char        *name;
    nodeptr     src;
    snkptr      snklist;
} elmdly;

typedef struct _elmdly_item *elmdly_item_ptr;

typedef struct _elmdly_item {
    elmdlyptr       elmdly;
    elmdly_item_ptr next;
} elmdly_item;

void print_help () {
    printf("NAME\n");
    printf("    rc2dly - convert qrouter RC output file to Vesta delay file\n\n");
    printf("SYNOPSIS\n");
    printf("    rc2dly -r <rc_file_name> -l <stdcell_liberty_file_name> -s <spef_file_name>\n");
    printf("\n");
    printf("DESCRIPTION\n");
    printf("    TBD\n");
    printf("Required Arguments\n");
    printf("    -r <rc_file_name>\n");
    printf("    -l <stdcell_liberty_file_name\n");
    printf("OPTIONS\n");
    printf("    -c <module_pin_capacitance_in_pF>\n");
    printf("\n");
}

char** tokenize_line (char *line, const char *delims, char*** tokens_ptr, int *num_toks) {
    int buff_sz = 4;

    char **tokens = calloc(buff_sz, sizeof(char*));

    int i = 0;

    tokens[i] = strtok(line, delims);
    i++;

    for (i = 1; tokens[i-1] != NULL; i++) {
        if (i == buff_sz) {
            buff_sz *= 2;
            tokens = realloc(tokens, sizeof(char*) * buff_sz);
        }
        *num_toks = i;
        tokens[i] = strtok(NULL, delims);
    }

    /**tokens_ptr = tokens;*/
    return tokens;
}

nodeptr create_node (char *name, int type, double nodeCap) {
    nodeptr new_node = calloc(1, sizeof(node));

    new_node->name = calloc(strlen(name) + 1, sizeof(char));
    strcpy(new_node->name, name);
    new_node->type = type;
    new_node->nodeCap = nodeCap;

    return new_node;
}

void add_node_item (node_item_ptr *node_item_list_ptr, nodeptr n, node_item_ptr *last_node_item) {

    node_item_ptr next = calloc(1, sizeof(node_item));
    next->node = n;

    // list has no items
    if (*node_item_list_ptr == NULL) {

        *node_item_list_ptr = next;

        if (last_node_item != NULL) {
            *last_node_item = next;
        }
    } else {

        // list has some items, we need to find the end
        if (last_node_item == NULL) {
            node_item_ptr i;

            for (i = *node_item_list_ptr; i->next != NULL; i = i->next);

            i->next = next;
            next->prev = i;
        } else {
            next->prev = *last_node_item;
            (*last_node_item)->next = next;
            *last_node_item = next;
        }
    }
}

void add_ritem (ritemptr *ritem_list_ptr, rptr r) {
    ritemptr next = calloc(1, sizeof(ritem));
    next->r = r;

    // list has no items
    if (*ritem_list_ptr == NULL) {

        *ritem_list_ptr = next;

    } else {

    // list has some items, we need to find the end
        ritemptr i;

        for (i = *ritem_list_ptr; i->next != NULL; i = i->next);

        i->next = next;
    }
}

void add_elmdly_item (elmdly_item_ptr *elmdly_item_list_ptr, elmdlyptr elmdly) {
    elmdly_item_ptr next = calloc(1, sizeof(elmdly_item));
    next->elmdly = elmdly;

    // list has no items
    if (*elmdly_item_list_ptr == NULL) {

        *elmdly_item_list_ptr = next;

    } else {

        // list has some items, we need to find the end
        elmdly_item_ptr i;

        for (i = *elmdly_item_list_ptr; i->next != NULL; i = i->next);

        i->next = next;
    }
}

// for multi-driver nets, must not recurse finding another driver
void sum_downstream_cap(nodeptr curr_node, nodeptr prev_node) {

    ritemptr curr_ritem = curr_node->rlist;

    while (curr_ritem != NULL) {
        // make sure to not backtrack to previous node
        // make sure to not recurse on the current node
        if (    (curr_ritem->r->node1 != prev_node)
            &&  (curr_ritem->r->node1 != curr_node)
           ) {

            sum_downstream_cap(curr_ritem->r->node1, curr_node);
            curr_node->totCapDownstream += (curr_ritem->r->node1->totCapDownstream + curr_ritem->r->node1->nodeCap);
	    if (curr_ritem->r->node1->type != SNK) {
		curr_node->totCapDownstreamLessGates += (curr_ritem->r->node1->totCapDownstreamLessGates + curr_ritem->r->node1->nodeCap);
	    }
        } else if (     (curr_ritem->r->node2 != prev_node)
                    &&  (curr_ritem->r->node2 != curr_node)
           ) {

            sum_downstream_cap(curr_ritem->r->node2, curr_node);
            curr_node->totCapDownstream += (curr_ritem->r->node2->totCapDownstream + curr_ritem->r->node2->nodeCap);
	    if (curr_ritem->r->node2->type != SNK) {
		curr_node->totCapDownstreamLessGates += (curr_ritem->r->node2->totCapDownstreamLessGates + curr_ritem->r->node2->nodeCap);
	    }
        }

        curr_ritem = curr_ritem->next;
    }
}

void add_snk (snkptr *snk_list_ptr, snkptr snk) {

    // list has no items
    if (*snk_list_ptr == NULL) {

        *snk_list_ptr = snk;

    } else {

        // list has some items, we need to find the end
        snkptr i;

        for (i = *snk_list_ptr; i->next != NULL; i = i->next);

        i->next = snk;
    }
}

void calculate_elmore_delay (
        nodeptr     curr_node,
        nodeptr     prev_node,
        rptr        prev_r, // the connection used to get curr_node
        elmdlyptr   curr_elmdly,
        /*snkptr      curr_snk,*/
        double      firstR,
        double      elmdly,
        int         verbose
        ) {

    // -recursively walk each branch of nodes
    // -accumulate delay on each branch
    // -append to Elmore Delay list when sink node reached

    // accumulate delay
    // -first node uses a model resistor based on typical output drive strengths
    //  of stdcell librarie
    // -subsequent nodes us the resistor that was traveled to arrive at current
    //  node

    if (verbose > 3) {
        fprintf(stdout, "INFO: node is %s with current delay of %.10f\n", curr_node->name, elmdly);
    }
    if (curr_node->type == SRC) {
        elmdly = firstR * (curr_node->nodeCap + curr_node->totCapDownstream);
        if (verbose > 3) {
            fprintf(stdout, "INFO: SRC node in elmore delay calc\n");
        }
    } else {
        if (verbose > 3) {
            fprintf(stdout, "INFO: not SRC node in elmore delay calc\n");
        }
        elmdly += prev_r->rval * (curr_node->nodeCap + curr_node->totCapDownstream);
    }

    // -if current node is an input to another cell, this is an endpoint and the
    //  current delay value needs to be saved
    // -there still might be other connections though that need to be traversed
    //  to find other endpoints
    if (curr_node->type == SNK) {

        if (verbose > 3) {
            printf("INFO: Found SNK node %s with delay to it of %.10f\n", curr_node->name, elmdly);
        }
        snkptr curr_snk = calloc(1, sizeof(snk));

        curr_snk->snknode = curr_node;
        curr_snk->delay = elmdly;

        add_snk(&curr_elmdly->snklist, curr_snk);
    }

    ritemptr curr_ritem = curr_node->rlist;

    while (curr_ritem != NULL) {
        // make sure to not backtrack to previous node
        // make sure to not recurse on the current node
        if (    (curr_ritem->r->node1 != prev_node)
            &&  (curr_ritem->r->node1 != curr_node)
           ) {

            calculate_elmore_delay(curr_ritem->r->node1, curr_node, curr_ritem->r, curr_elmdly, firstR, elmdly, verbose);
            if (verbose > 1) printf("TEST: %s %f %f\n", curr_node->name, curr_node->nodeCap, curr_node->totCapDownstream);

        } else if (     (curr_ritem->r->node2 != prev_node)
                    &&  (curr_ritem->r->node2 != curr_node)
           ) {

            calculate_elmore_delay(curr_ritem->r->node2, curr_node, curr_ritem->r, curr_elmdly, firstR, elmdly, verbose);
            if (verbose > 1) printf("TEST: %s %f %f\n", curr_node->name, curr_node->nodeCap, curr_node->totCapDownstream);

        }

        curr_ritem = curr_ritem->next;
    }
}

int main (int argc, char* argv[]) {

    FILE* outfile = stdout;
    FILE* libfile = NULL;
    FILE* rcfile = NULL;
    FILE* speffile = stdout;

    int verbose = 4;

    double modulePinCapacitance = 0;

    Cell *cells, *newcell;
    Pin *newpin;
    char* libfilename;

    nodeptr currnode = NULL;
    rptr    currR    = NULL;
    snkptr currSnk = NULL;

    // pointer to last node in a doubly-linked list consisting of node_items
    node_item_ptr currNodeStack = NULL;
    node_item_ptr allNodes = NULL;
   
    // -Maintain a list of all nodes that are outputs / drivers.
    // -Iterate over the list to walk each interconnect to calculate
    //  Elmore Delay
    node_item_ptr drivers = NULL;
    node_item_ptr last_driver = NULL;
    int numDrivers = 0;

    // list of all Rs for debugging and to easily free them at end
    ritemptr allrs = NULL;

    elmdly_item_ptr delays = NULL;

    // Command-line argument parsing
    int c;

    while (1) {
        static struct option long_options[] = {
            {"rc-file"      , required_argument , 0, 'r'},
            {"liberty-file" , required_argument , 0, 'l'},
            {"spef-file"   , required_argument , 0, 's'},
            {"pin-capacitance"   , required_argument , 0, 'c'},
            {"verbose"      , required_argument , 0, 'v'},
            {"help"         , no_argument       , 0, 'h'},
            {0, 0, 0, 0}
        };

        /* getopt_long stores the option index here. */
        int option_index = 0;

        c = getopt_long (argc, argv, "hv:r:l:s:", long_options, &option_index);

        /* Detect the end of the options. */
        if (c == -1)
            break;

        switch (c) {
            case 0:
                /* If this option set a flag, do nothing else now. */
                if (long_options[option_index].flag != 0)
                    break;
                printf ("option %s", long_options[option_index].name);
                if (optarg)
                    printf (" with arg %s", optarg);
                printf ("\n");
                break;

            case 'r':
                rcfile = fopen(optarg, "r");

                if (!rcfile) {
                    fprintf(stderr, "ERROR: Unable to open input RC file `%s': %s\n", optarg, strerror(errno));
                }
                break;

            case 'l':
                libfile = fopen(optarg, "r");
                libfilename = strdup(optarg);

                if (!libfile) {
                    fprintf(stderr, "ERROR: Unable to open input Liberty Timing file`%s': %s\n", optarg, strerror(errno));
                }
                break;

            case 'c':
                modulePinCapacitance = atof(optarg);
                break;

            case 'h':
                print_help();
                break;

            case 'v':
                verbose = atoi(optarg);
                break;

            case 's':
                if (!strcmp(optarg, "-")) {
                    speffile = stdout;
                } else {
                    speffile = fopen(optarg, "w");
                }
                if (!speffile) {
                    fprintf(stderr, "ERROR: Unable to open speffile`%s': %s\n", optarg, strerror(errno));
                }
                break;

            default:
                print_help();
                return 0;
        }
    }

    if (rcfile == NULL) {
        fprintf(stderr, "ERROR: Must specify input RC file.\n");
        return 1;
    }
    if (libfile == NULL) {
        fprintf(stderr, "ERROR: Must specify input Liberty Timing file.\n");
        return 1;
    }
    fclose(libfile);

    // Read in Liberty File
    printf("Reading Liberty file %s\n", libfilename);
    cells = read_liberty(libfilename, 0);

    if (cells == NULL) return 5;

    if (verbose > 3) {
        for (newcell = cells; newcell; newcell = newcell->next) {
	    if (newcell->name == NULL) continue;  /* "don't use" cell */
            fprintf(stdout, "Cell: %s\n", newcell->name);
            fprintf(stdout, "   Function: %s\n", newcell->function);
            for (newpin = newcell->pins; newpin; newpin = newpin->next) {
                fprintf(stdout, "   Pin: %s  cap=%g\n", newpin->name, newpin->cap);
            }
            fprintf(stdout, "\n");
        }
    }

    char *line;
    size_t nbytes = LIB_LINE_MAX;
    line = calloc(1, LIB_LINE_MAX);
    int bytesRead = 0;

    const char delims[3] = " \n";

    char **tokens;
    int num_toks = 0;

    bytesRead = getline(&line, &nbytes, rcfile);

    // <net> <num_net_drivers> <driver_node_0> [drive_node_n] <num_receivers> (R1 C1
    // <terminal>, R2 C2 <terminal>, ...)
    //
    // Parsing States for .rc file
    // 1) net / interconnect name
    // 2) num drivers
    // 3) process listed drivers
    // 4) num receivers
    //

    int num_net_drivers = 0;
    int num_rxers = 0;
    int t = 0;
    Cell *cell;
    node_item_ptr tmp_nip = NULL;

    fprintf(speffile, "*SPEF \"IEEE 1481-1998\"\n*VERSION \"0.0\"\n*DESIGN_FLOW \"NETLIST_TYPE_VERILOG\"\n*DIVIDER /\n*DELIMITER :\n*BUS_DELIMITER []\n*T_UNIT 1 PS\n*C_UNIT 1 PF\n*R_UNIT 1 OHM\n");
    while (bytesRead > 0) {
        float total_Cap = 0;
        // skip blank lines
        if (bytesRead > 2) {
            ritemptr allNetRs = NULL;
            node_item_ptr allNetNodes = NULL;
            tokens = tokenize_line(line, delims, &tokens, &num_toks);

            t = 0;

	    if (verbose > 3)
                fprintf(stdout, "\nProcessing net %s\n", tokens[0]);
       
            fprintf(speffile, "*D_NET %s ", tokens[0]);
            t += 1;

            // process number of drivers
            num_net_drivers = atoi(tokens[t]);
            //fprintf(stdout, "Number of drivers is %d\n", num_net_drivers);
            t += 1;

            // process drivers
            for (; t < (2 + num_net_drivers); t++) {
	        if (verbose > 3)
                    fprintf(stdout, "TBD: process driver number %d %s\n", t-2, tokens[t]);
            }

            // no t increment is required as for loop gets us to proper index after last driver
            num_rxers = atoi(tokens[t]);
            t += 1;

            // process remaining tokens which contains R's, C's, node connections, and rxers
            int nodeNum = 0;
            int rNum = 0;
            char *name = NULL;

            while(t < num_toks) {

                if (!strcmp(tokens[t], "(")) {

                    // check if this is the first node
                    if (nodeNum == 0) {

                        // assemble node name based on interconnect name and node number
                        name = calloc(1, sizeof(char) * (strlen(tokens[0]) + 10));

                        if (sprintf(name, "%s_n%d", tokens[0], nodeNum) < 0) {
                            fprintf(stderr, "ERROR: sprintf failed to create interconnect node name\n");
                            return 2;
                        }

                        // create a new node, this one is the first (driving) node of the interconnect
                        currnode = create_node(tokens[2], SRC, 0);
                        total_Cap += currnode->nodeCap;
                        printf("\ntotal_Cap: %lf",total_Cap);
                        if (verbose > 1) print_node(currnode);

                        // add node to list of drivers
                        add_node_item(&drivers, currnode, &last_driver);
                        numDrivers += 1;

                        // add node to current node stack
                        add_node_item(&currNodeStack, currnode, &currNodeStack);
                        add_node_item(&allNodes, currnode, NULL);
                        add_node_item(&allNetNodes, currnode, NULL);
                        //printf("%s_n%d\n", tokens[0], nodeNum);

                        nodeNum += 1;
                    }

                    name = calloc(1, sizeof(char) * (strlen(tokens[0]) + 10));
                    if (sprintf(name, "%s_n%d", tokens[0], nodeNum) < 0) {
                        fprintf(stderr, "ERROR: sprintf failed to create interconnect node name\n");
                        return 2;
                    }
                    nodeNum += 1;
                    // create the new node
                    currnode = create_node(name, INT, atof(tokens[t+2]));
                    total_Cap += currnode->nodeCap;
                    printf("\ntotal_Cap: %lf",total_Cap);
                    if (verbose > 1) {
                        print_node(currnode);
                        fprintf(stdout, "nodeCap of new node is %.10f\n", atof(tokens[t+2]));
                    }

                    name = calloc(1, sizeof(char) * (strlen(tokens[0]) + 10));
                    if (sprintf(name, "%s_r%d", tokens[0], rNum) < 0) {
                        fprintf(stderr, "ERROR: sprintf failed to create resistor name\n");
                        return 2;
                    }
                    rNum += 1;
                    // create resistor
                    currR = calloc(1, sizeof(r));
                    currR->name = name;
                    currR->node1 = currNodeStack->node;
                    currR->node2 = currnode;
                    currR->rval = atof(tokens[t+1]);
                    // add resistor to each node's resistor list and the global list
                    add_ritem(&currNodeStack->node->rlist, currR);
                    add_ritem(&currnode->rlist, currR);
                    add_ritem(&allrs, currR);
                    add_ritem(&allNetRs, currR);
                    fprintf(stdout, "*****add res between %s and %s with value %lf\n", currNodeStack->node->name, currnode->name, currR->rval);
                    // push the most recent node onto the nodestack
                    add_node_item(&currNodeStack, currnode, &currNodeStack);
                    add_node_item(&allNodes, currnode, NULL);
                    add_node_item(&allNetNodes, currnode, NULL);
                    //if (verbose > 2) fprintf(stdout, "Add node %s\n", currnode->name);

                    t += 3;

                } else if (!strcmp(tokens[t], ")")) {
                    // pop the top node off the nodestack
                    if (currNodeStack != NULL) {
                        if (verbose > 2) fprintf(stdout, "Pop node %s\n", currNodeStack->node->name);
                        tmp_nip = currNodeStack;
                        currNodeStack = currNodeStack->prev;
                        currNodeStack->next = NULL;
                        free(tmp_nip);
                    } else {
                        fprintf(stderr, "ERROR: Attempt to pop an empty current node stack!\n");
                        return 3;
                    }

                    t += 1;
                } else if (!strcmp(tokens[t], ",")) {
                    // nothing to do on a comma
                    t += 1;
                } else {
                    // located a receiver
                    // Some of the receiver nodes are not endpoints of a branch,
                    // but are branch points themselves. This complicates how
                    // to label the node as a SRC, INT, or SNK node since the
                    // Elmore Delay calculation looks at the node type to
                    // determine when it has reached an endpoint.
                    //
                    // The solution to this is to create an extra node when a
                    // receiver is found that is connected via a 0 ohm resistor.
                    // The capacitance on this node (the receiver input capacitance)
                    // will be absorbed as downstream capacitance with the 0 ohm
                    // R contributing nothing

                    // create node name
                    // name the extra node after the receiver
                    name = strdup(tokens[t]);

                    // create the new node
                    currnode = create_node(name, SNK, 0);
                    total_Cap += currnode->nodeCap;
                    printf("\ntotal_Cap: %lf",total_Cap);
                    if (verbose > 1) print_node(currnode);
                    name = calloc(1, sizeof(char) * (strlen(tokens[0]) + 10));
                    if (sprintf(name, "%s_r%d", tokens[0], rNum) < 0) {
                        fprintf(stderr, "ERROR: sprintf failed to create resistor name\n");
                        return 2;
                    }
                    rNum += 1;
                    // create resistor
                    currR = calloc(1, sizeof(r));
                    currR->name = name;
                    currR->node1 = currNodeStack->node;
                    currR->node2 = currnode;
                    currR->rval = 0;
                    // add resistor to each node's resistor list and the global list
                    add_ritem(&currNodeStack->node->rlist, currR);
                    add_ritem(&currnode->rlist, currR);
                    add_ritem(&allrs, currR);

                    // Add the receiver contributed capacitance which is either
                    // the input pin capacitance to a std cell or the user-specified
                    // capacitance of a module-level pin
                    char *cellIndex = strsep(&tokens[t], "/");
                    char *cellName = strsep(&cellIndex, "_");
                    char *pinName = tokens[t];

                    if (!strcmp(cellName, "PIN")) {
                        currnode->nodeCap = modulePinCapacitance;
                        //fprintf(stdout, "Found pin as receiver: %s\n", tokens[t]);
                    } else {

                        cell = get_cell_by_name(cells, cellName);
                        Pin *tmpPin = NULL;

                        if (cell != NULL) {
                            tmpPin = get_pin_by_name(cell, pinName);
                            // Liberty Timing File cap units are in pf for osu std cells (other possibility is ff)
                            // readliberty.c stores them and returns values as ff
                            // -> need to correct by /1000 to put back in pf
                            currnode->nodeCap = tmpPin->cap/1000;

                            if (verbose > 3) {
                                printf("cap is %f\n", tmpPin->cap);
                                fprintf(stdout, "INFO: Found cell as receiver: %s\n", cell->name);
                                fprintf(stdout, "INFO: Added cap value is %s %f\n\n", tmpPin->name, tmpPin->cap/1000);
                                print_node(currnode);
                            }
                        } else {
                            if (verbose > 3) {
                                fprintf(stdout, "INFO: Skipping lineAdded cap value is %s %f\n", tmpPin->name, tmpPin->cap/1000);
                            }
                        }
                    }
                    total_Cap += currnode->nodeCap;
                    printf("\ntotal_Cap: %lf",total_Cap);
                    // The extra node created to handle termination points in the
                    // interconnect does not need to be pushed onto the stack

                    // but still add to full node list
                    //if (verbose > 2) fprintf(stdout, "Add node %s\n", currnode->name);
                    add_node_item(&allNodes, currnode, NULL);
                    add_node_item(&allNetNodes, currnode, NULL);

                    t += 1;
                }
            }

            if (verbose > 3)
                fprintf(stdout, "INFO: Verify all nodes matched up by balancing the parens\n");
            // Verify we matched up all the nodes by popping off the driver node
            if (currNodeStack != NULL) {
                tmp_nip = currNodeStack;
                currNodeStack = currNodeStack->prev;
                free(tmp_nip);
            } else {
                fprintf(stdout, "ERROR: Attempt to pop an empty current node stack!\n");
                return 3;
            }

            if (currNodeStack != NULL) {
                fprintf(stderr, "ERROR: Net %s had unbalance parentheses!\n", tokens[0]);
                return 4;
            }

            if (verbose > 3)
                fprintf(stdout, "INFO: Sum downstream capacitance for each node\n");
            sum_downstream_cap(last_driver->node, NULL);

            if (verbose > 3) print_node(last_driver->node);

            node_item_ptr nodeConn_itr = allNetNodes;
            node_item_ptr nodeCap_itr = allNetNodes;
            node_item_ptr nodeRes_itr = allNetNodes;
            fprintf(speffile,"%lf\n",total_Cap);
            fprintf(speffile, "*CONN\n");
                int firstNode = 1;
                node_item_ptr tmp_node = nodeConn_itr;
                nodeptr temp_n = NULL;
                while(nodeConn_itr != NULL) {
                  temp_n = nodeConn_itr->node;
                  char *nodeName = temp_n->name;
                  char *itr;
                  for(itr=nodeName; *itr; itr++)
                  {
                    if (*itr == '/')
                    {
                       *itr = ':'; 
                    
                      if(*nodeName == 'P')
                      {
                        nodeName++;
                        if (*nodeName == 'I')
                          nodeName++;
                        if (*nodeName =='N')
                        {
                          nodeName+=2;
                          temp_n->name = nodeName;
                          if (firstNode)
                            fprintf(speffile, "*P %s O\n", temp_n->name);
                          else
                            fprintf(speffile, "*P %s I\n", temp_n->name);
                        }
                      }
                      else
                      {
                         if (firstNode)
                           fprintf(speffile, "*I %s O\n", temp_n->name);
                         else
                           fprintf(speffile, "*I %s I\n", temp_n->name);
                      }
                    }
                  }
                  nodeConn_itr = nodeConn_itr->next;
                  firstNode = 0;
                }

                fprintf(speffile,"*CAP\n");
                int count = 1;
                while(nodeCap_itr != NULL) {
                  temp_n = nodeCap_itr->node;
                  fprintf(speffile, "%d %s %lf\n", count, temp_n->name, temp_n->nodeCap);
                  count++;
                  nodeCap_itr = nodeCap_itr->next;
                }
                ritemptr tmp_res = allNetRs;
                rptr tmp_r = NULL;
                int count2 = 1;
                fprintf(speffile,"*RES\n");             
                while(tmp_res != NULL) {
                  tmp_r = tmp_res->r;
                  fprintf(speffile, "%d %s %s %lf\n", count2, tmp_r->node1->name,tmp_r->node2->name,tmp_r->rval);
                  tmp_res = tmp_res->next;
                  count2++;
                }

                fprintf(speffile,"*END\n");
                 

            /*elmdlyptr currElm = calloc(1, sizeof(elmdly));
            currElm->name = calloc(1, sizeof(char) * strlen(tokens[0]));
            // name the Elmore Delay after the net
            strcpy(currElm->name, tokens[0]);
            currElm->src = last_driver->node;
            add_elmdly_item(&delays, currElm);

            if (verbose > 3) {
                fprintf(stdout, "INFO: Calculate Elmore Delay for each SNK\n");
            }
            calculate_elmore_delay(
                                    last_driver->node,
                                    NULL,
                                    NULL,
                                    currElm,
                                    //NULL,
                                    1,
                                    0,
                                    verbose
                                    );

            if (verbose > 3) fprintf(stdout, "ELM: %s\t\t%s\t\t%f\n", currElm->name, currElm->src->name, currElm->src->nodeCap + currElm->src->totCapDownstream);
            fprintf(outfile, "%s\n", currElm->name);
            fprintf(outfile, "%s %f\n", currElm->src->name, currElm->src->totCapDownstreamLessGates);
 
            currSnk = currElm->snklist;
 
            while(currSnk != NULL) {
                fprintf(outfile, "%s %f\n", currSnk->snknode->name, currSnk->delay);
                currSnk = currSnk->next;
            }
 
            fprintf(outfile, "\n");*/
        }

        bytesRead = getline(&line, &nbytes, rcfile);
    }

    fclose(outfile);
    fclose(speffile);
    // Cleanup

    free(delays);

    ritemptr tmp_ritem = allrs;
    rptr tmp_r = NULL;
    int numRs = 0;

    while(allrs != NULL) {
        numRs++;
        tmp_ritem = allrs->next;
        free(allrs->r->name);
        free(allrs->r);
        free(allrs);
        allrs = tmp_ritem;
    }
    printf("Number of Rs: %d\n", numRs);

    fprintf(stdout, "TBD: need to clean-up node deletion\n");
    fclose(rcfile);

    return 0;
}
