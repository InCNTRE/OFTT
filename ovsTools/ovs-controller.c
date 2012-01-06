/*
 * Copyright (c) 2008, 2009, 2010 Nicira Networks.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at:
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include <config.h>

#include <errno.h>
#include <getopt.h>
#include <limits.h>
#include <signal.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <netinet/in.h> //Junos changes



#include "command-line.h"
#include "compiler.h"
#include "daemon.h"
#include "learning-switch.h"
#include "ofpbuf.h"
#include "openflow/openflow.h"
#include "poll-loop.h"
#include "rconn.h"
#include "stream-ssl.h"
#include "timeval.h"
#include "unixctl.h"
#include "util.h"
#include "vconn.h"
#include "vlog.h"
#include "xtoxll.h"
#include "ovs-common.h"

VLOG_DEFINE_THIS_MODULE(controller)

#define MAX_SWITCHES 16
#define MAX_LISTENERS 16

struct switch_ {
    struct lswitch *lswitch;
    struct rconn *rconn;
};

/* Learn the ports on which MAC addresses appear? */
static bool learn_macs = true;

/* Set up flows?  (If not, every packet is processed at the controller.) */
static bool set_up_flows = true;

/* -N, --normal: Use "NORMAL" action instead of explicit port? */
static bool action_normal = false;

/* -w, --wildcard: Set up exact match or wildcard flow entries? */
static bool exact_flows = true;

/* --max-idle: Maximum idle time, in seconds, before flows expire. */
static int max_idle = 60;

/* --mute: If true, accept connections from switches but do not reply to any
 * of their messages (for debugging fail-open mode). */
static bool mute = false;

/* -q, --queue: OpenFlow queue to use, or the default queue if UINT32_MAX. */
static uint32_t queue_id = UINT32_MAX;

/* --with-flows: File with flows to send to switch, or null to not load
 * any default flows. */
static FILE *flow_file = NULL;

/* --unixctl: Name of unixctl socket, or null to use the default. */
static char *unixctl_path = NULL;

static int do_switching(struct switch_ *);
static void new_switch(struct switch_ *, struct vconn *);
static void parse_options(int argc, char *argv[]);
static void usage(void) NO_RETURN;

struct ofpbuf * make_unbuffered_packet_out(const struct ofpbuf *packet, uint16_t in_port, uint16_t out_port);

//Application currently does not support more than one switch
struct switch_ our_switch;

void unixctl_cb_flow_add(struct unixctl_conn * conn, const char *args, void *aux OVS_UNUSED);
void unixctl_cb_flow_del(struct unixctl_conn * conn, const char *args, void *aux OVS_UNUSED);
void unixctl_cb_packet_out(struct unixctl_conn * conn, const char *args, void *aux OVS_UNUSED);

void send_flow_add(struct lswitch *sw, struct rconn *rconn, const char * args);
void send_flow_del(struct lswitch *sw, struct rconn *rconn, const char * args);
void send_packet_out(struct lswitch *sw, struct rconn *rconn, const char * args);

void 
unixctl_cb_flow_add(struct unixctl_conn * conn, const char *args, void *aux OVS_UNUSED)
{
    VLOG_INFO("Request junos-add-flow received from ovs-ofctl: %s", args);

    send_flow_add(our_switch.lswitch, our_switch.rconn, args);

    unixctl_command_reply(conn, 200, NULL);
    
}

void
unixctl_cb_flow_del(struct unixctl_conn * conn, const char *args, void *aux OVS_UNUSED)
{
    VLOG_INFO("Request junos-del-flow received from ovs-ofctl: %s", args);

    send_flow_del(our_switch.lswitch, our_switch.rconn, args);

    unixctl_command_reply(conn, 200, NULL);

}

void
unixctl_cb_packet_out(struct unixctl_conn * conn, const char *args, void *aux OVS_UNUSED)
{
    VLOG_INFO("Request junos-packet-out received from ovs-ofctl: %s", args);

    send_packet_out(our_switch.lswitch, our_switch.rconn, args);

    unixctl_command_reply(conn, 200, NULL);

}

int
main(int argc, char *argv[])
{
    struct unixctl_server *unixctl;
    struct switch_ switches[MAX_SWITCHES];
    struct pvconn *listeners[MAX_LISTENERS];
    int n_switches, n_listeners;
    int retval;
    int i;

    proctitle_init(argc, argv);
    set_program_name(argv[0]);
    parse_options(argc, argv);
    signal(SIGPIPE, SIG_IGN);

    if (argc - optind < 1) {
        ovs_fatal(0, "at least one vconn argument required; "
                  "use --help for usage");
    }

    n_switches = n_listeners = 0;
    for (i = optind; i < argc; i++) {
        const char *name = argv[i];
        struct vconn *vconn;
        int retval;

        retval = vconn_open(name, OFP_VERSION, &vconn);
        if (!retval) {
            if (n_switches >= MAX_SWITCHES) {
                ovs_fatal(0, "max %d switch connections", n_switches);
            }
            new_switch(&switches[n_switches++], vconn);
            continue;
        } else if (retval == EAFNOSUPPORT) {
            struct pvconn *pvconn;
            retval = pvconn_open(name, &pvconn);
            if (!retval) {
                if (n_listeners >= MAX_LISTENERS) {
                    ovs_fatal(0, "max %d passive connections", n_listeners);
                }
                listeners[n_listeners++] = pvconn;
            }
        }
        if (retval) {
            VLOG_ERR("%s: connect: %s", name, strerror(retval));
        }
    }
    if (n_switches == 0 && n_listeners == 0) {
        ovs_fatal(0, "no active or passive switch connections");
    }

    die_if_already_running();
    daemonize_start();

    retval = unixctl_server_create(unixctl_path, &unixctl);
    if (retval) {
        exit(EXIT_FAILURE);
    }

    //Register unixctl commands
    unixctl_command_register(JUNOS_ADD_FLOW_CMD, unixctl_cb_flow_add, NULL); // Junos changes
    unixctl_command_register(JUNOS_DEL_FLOW_CMD, unixctl_cb_flow_del, NULL); // Junos changes
    unixctl_command_register(JUNOS_PACKET_OUT, unixctl_cb_packet_out, NULL); // Junos changes

    daemonize_complete();

    while (n_switches > 0 || n_listeners > 0) {
        int iteration;
        int i;

        

        /* Accept connections on listening vconns. */
        for (i = 0; i < n_listeners && n_switches < MAX_SWITCHES; ) {
            struct vconn *new_vconn;
            int retval;

            retval = pvconn_accept(listeners[i], OFP_VERSION, &new_vconn);
            if (!retval || retval == EAGAIN) {
                if (!retval) {
                    new_switch(&switches[n_switches++], new_vconn);
                }
                i++;
            } else {
                pvconn_close(listeners[i]);
                listeners[i] = listeners[--n_listeners];
            }
        }

        /* Do some switching work.  Limit the number of iterations so that
         * callbacks registered with the poll loop don't starve. */
        for (iteration = 0; iteration < 50; iteration++) {
            bool progress = false;
            for (i = 0; i < n_switches; ) {
                struct switch_ *this = &switches[i];

                //TODO: add support for more than one switch
                if(this)
                	our_switch = *this;

                int retval = do_switching(this);
                if (!retval || retval == EAGAIN) {
                    if (!retval) {
                        progress = true;
                    }
                    i++;
                } else {
                    rconn_destroy(this->rconn);
                    lswitch_destroy(this->lswitch);
                    switches[i] = switches[--n_switches];
                }
            }
            if (!progress) {
                break;
            }
        }
        for (i = 0; i < n_switches; i++) {
            struct switch_ *this = &switches[i];
            lswitch_run(this->lswitch);
        }

        unixctl_server_run(unixctl);

        /* Wait for something to happen. */
        if (n_switches < MAX_SWITCHES) {
            for (i = 0; i < n_listeners; i++) {
                pvconn_wait(listeners[i]);
            }
        }
        for (i = 0; i < n_switches; i++) {
            struct switch_ *sw = &switches[i];
            rconn_run_wait(sw->rconn);
            rconn_recv_wait(sw->rconn);
            lswitch_wait(sw->lswitch);
        }
        unixctl_server_wait(unixctl);
        poll_block();
    }

    return 0;
}

static void
new_switch(struct switch_ *sw, struct vconn *vconn)
{
    sw->rconn = rconn_create(60, 0);
    rconn_connect_unreliably(sw->rconn, vconn, NULL);

    /* If it was set, rewind 'flow_file' to the beginning, since a
     * previous call to lswitch_create() will leave the stream at the
     * end. */
    if (flow_file) {
        rewind(flow_file);
    }
    sw->lswitch = lswitch_create(sw->rconn, learn_macs, exact_flows,
                                 set_up_flows ? max_idle : -1,
                                 action_normal, flow_file);

    lswitch_set_queue(sw->lswitch, queue_id);
}

static int
do_switching(struct switch_ *sw)
{
    unsigned int packets_sent;
    struct ofpbuf *msg;

    packets_sent = rconn_packets_sent(sw->rconn);

    msg = rconn_recv(sw->rconn);
    if (msg) {
        if (!mute) {
            lswitch_process_packet(sw->lswitch, sw->rconn, msg);
        }
        ofpbuf_delete(msg);
    }
    rconn_run(sw->rconn);

    return (!rconn_is_alive(sw->rconn) ? EOF
            : rconn_packets_sent(sw->rconn) != packets_sent ? 0
            : EAGAIN);
}

static void
parse_options(int argc, char *argv[])
{
    enum {
        OPT_MAX_IDLE = UCHAR_MAX + 1,
        OPT_PEER_CA_CERT,
        OPT_MUTE,
        OPT_WITH_FLOWS,
        OPT_UNIXCTL,
        VLOG_OPTION_ENUMS
    };
    static struct option long_options[] = {
        {"hub",         no_argument, 0, 'H'},
        {"noflow",      no_argument, 0, 'n'},
        {"normal",      no_argument, 0, 'N'},
        {"wildcard",    no_argument, 0, 'w'},
        {"max-idle",    required_argument, 0, OPT_MAX_IDLE},
        {"mute",        no_argument, 0, OPT_MUTE},
        {"queue",       required_argument, 0, 'q'},
        {"with-flows",  required_argument, 0, OPT_WITH_FLOWS},
        {"unixctl",     required_argument, 0, OPT_UNIXCTL},
        {"help",        no_argument, 0, 'h'},
        {"version",     no_argument, 0, 'V'},
        DAEMON_LONG_OPTIONS,
        VLOG_LONG_OPTIONS,
#ifdef HAVE_OPENSSL
        STREAM_SSL_LONG_OPTIONS
        {"peer-ca-cert", required_argument, 0, OPT_PEER_CA_CERT},
#endif
        {0, 0, 0, 0},
    };
    char *short_options = long_options_to_short_options(long_options);

    for (;;) {
        int indexptr;
        int c;

        c = getopt_long(argc, argv, short_options, long_options, &indexptr);
        if (c == -1) {
            break;
        }

        switch (c) {
        case 'H':
            learn_macs = false;
            break;

        case 'n':
            set_up_flows = false;
            break;

        case OPT_MUTE:
            mute = true;
            break;

        case 'N':
            action_normal = true;
            break;

        case 'w':
            exact_flows = false;
            break;

        case OPT_MAX_IDLE:
            if (!strcmp(optarg, "permanent")) {
                max_idle = OFP_FLOW_PERMANENT;
            } else {
                max_idle = atoi(optarg);
                if (max_idle < 1 || max_idle > 65535) {
                    ovs_fatal(0, "--max-idle argument must be between 1 and "
                              "65535 or the word 'permanent'");
                }
            }
            break;

        case 'q':
            queue_id = atoi(optarg);
            break;

        case OPT_WITH_FLOWS:
            flow_file = fopen(optarg, "r");
            if (flow_file == NULL) {
                ovs_fatal(errno, "%s: open", optarg);
            }
            break;

        case OPT_UNIXCTL:
            unixctl_path = optarg;
            break;

        case 'h':
            usage();

        case 'V':
            OVS_PRINT_VERSION(OFP_VERSION, OFP_VERSION);
            exit(EXIT_SUCCESS);

        VLOG_OPTION_HANDLERS
        DAEMON_OPTION_HANDLERS

#ifdef HAVE_OPENSSL
        STREAM_SSL_OPTION_HANDLERS

        case OPT_PEER_CA_CERT:
            stream_ssl_set_peer_ca_cert_file(optarg);
            break;
#endif

        case '?':
            exit(EXIT_FAILURE);

        default:
            abort();
        }
    }
    free(short_options);
}

void
send_flow_add(struct lswitch *sw, struct rconn *rconn,
                   const char * args)
{
        struct ofpbuf *b;
        struct ofp_flow_mod *ofm;
        uint16_t priority, idle_timeout, hard_timeout;
        uint64_t cookie;
        struct ofp_match match;

        /* Parse and send.  str_to_flow() will expand and reallocate the data
         * in 'buffer', so we can't keep pointers to across the str_to_flow()
         * call. */
        make_openflow(sizeof *ofm, OFPT_FLOW_MOD, &b);
        parse_ofp_str(args, &match, b,
                      NULL, NULL, &priority, &idle_timeout, &hard_timeout,
                      &cookie);
        ofm = b->data;
        ofm->match = match;
        ofm->command = htons(OFPFC_ADD);
        ofm->cookie = htonll(cookie);
        ofm->idle_timeout = htons(idle_timeout);
        ofm->hard_timeout = htons(hard_timeout);
        ofm->buffer_id = htonl(UINT32_MAX);
        ofm->priority = htons(priority);

        update_openflow_length(b);
        queue_tx(sw, rconn, b);
}


void send_flow_del(struct lswitch *sw, struct rconn *rconn,
                       const char * args)
{
    uint16_t priority;
    uint16_t out_port;
    struct ofpbuf *b;
    struct ofp_flow_mod *ofm;
    struct ofp_match match;

    /* Parse and send. */
    make_openflow(sizeof *ofm, OFPT_FLOW_MOD, &b);
    parse_ofp_str(args, &match, NULL, NULL,
                  &out_port, &priority, NULL, NULL, NULL);

//    if (strict) {
//        ofm->command = htons(OFPFC_DELETE_STRICT);
//   } else {
//        ofm->command = htons(OFPFC_DELETE);
//    }

    ofm = b->data;
    ofm->match = match;
    ofm->command = htons(OFPFC_DELETE);
    ofm->idle_timeout = htons(0);
    ofm->hard_timeout = htons(0);
    ofm->buffer_id = htonl(UINT32_MAX);
    ofm->out_port = htons(out_port);
    ofm->priority = htons(priority);

    update_openflow_length(b);
    queue_tx(sw, rconn, b);
}


void send_packet_out(struct lswitch *sw, struct rconn *rconn,
                    const char * args)
{
    struct ofpbuf *b;
    struct ofpbuf *packet;
    char *tmp;
    uint16_t output_port;

    VLOG_INFO("Args: %s", args);

    output_port = parse_packet_out_params(args);

    packet = ofpbuf_new(64);
    packet->size = 64;
    memset(packet->data, 0x00, 64); 

    b = make_unbuffered_packet_out(packet, ODPP_LOCAL, output_port);
    update_openflow_length(b);
    queue_tx(sw, rconn, b);

}

static void
usage(void)
{
    printf("%s: OpenFlow controller\n"
           "usage: %s [OPTIONS] METHOD\n"
           "where METHOD is any OpenFlow connection method.\n",
           program_name, program_name);
    vconn_usage(true, true, false);
    daemon_usage();
    vlog_usage();
    printf("\nOther options:\n"
           "  -H, --hub               act as hub instead of learning switch\n"
           "  -n, --noflow            pass traffic, but don't add flows\n"
           "  --max-idle=SECS         max idle time for new flows\n"
           "  -N, --normal            use OFPAT_NORMAL action\n"
           "  -w, --wildcard          use wildcards, not exact-match rules\n"
           "  -q, --queue=QUEUE       OpenFlow queue ID to use for output\n"
           "  --with-flows FILE       use the flows from FILE\n"
           "  --unixctl=SOCKET        override default control socket name\n"
           "  -h, --help              display this help message\n"
           "  -V, --version           display version information\n");
    exit(EXIT_SUCCESS);
}
