/*
 * ipmirror.{cc,hh} -- rewrites IP packet a->b to b->a
 * Max Poletto
 *
 * Copyright (c) 2000 Massachusetts Institute of Technology.
 *
 * This software is being provided by the copyright holders under the GNU
 * General Public License, either version 2 or, at your discretion, any later
 * version. For more information, see the `COPYRIGHT' file in the source
 * distribution.
 */

#ifdef HAVE_CONFIG_H
# include <config.h>
#endif
#include "ipmirror.hh"
#include "click_ip.h"
#include "click_udp.h"

void
IPMirror::push(int, Packet *p)
{
  p = p->uniqueify();
  // new checksum is same as old checksum
  
  click_ip *iph = p->ip_header();
  struct in_addr tmpa = iph->ip_src;
  iph->ip_src = iph->ip_dst;
  iph->ip_dst = tmpa;
  
  click_udp *udph = (click_udp *)(iph + 1);
  unsigned short tmpp = udph->uh_sport;
  udph->uh_sport = udph->uh_dport;
  udph->uh_dport = tmpp;
  
  output(0).push(p);
}

EXPORT_ELEMENT(IPMirror)
