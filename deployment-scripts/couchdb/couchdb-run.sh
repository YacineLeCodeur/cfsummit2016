#!/bin/bash
echo
echo "### Starting couchdb-run.sh ###"
echo

echo "environment = ${ENVIRONMENT}"

# for openstack as environment
if [ "$ENVIRONMENT" = 'openstack' ]; then
  $OPENSTACK_START
fi

echo "  ┌────────────────────────────────────────────────────────────────┬─────────────────┐"
echo "  │   ┬ ┬ ┬ ┬ ┬ ┬    ╔══╗  ╦   ╦  ╔══╗  ╦  ╦    ╔══╗     ┌┬┐ ┌─┐   │                 │"
echo "  │   │││ │││ │││    ║═╣   ╚╗ ╔╝  ║  ║  ║  ║    ╠══╣      ││ ├┤    │   evoila GmbH   │"
echo "  │   └┴┘ └┴┘ └┴┘ o  ╚══╝   ╚═╝   ╚══╝  ╩  ╩══╝ ╩  ╩  o  ─┴┘ └─┘   │ Mainz / Germany │"
echo "  │                                                                │                 │"
echo "  │    ┌─┐┌─┐┬─┐┬  ┬┬┌─┐┌─┐  ┬┌─┐  ┌─┐┌┬┐┌─┐┬─┐┌┬┐┬┌┐┌┌─┐          │  www.evoila.de  │"
echo "  │    └─┐├┤ ├┬┘└┐┌┘││  ├┤   │└─┐  └─┐ │ ├─┤├┬┘ │ │││││ ┬          │ info@evoila.de  │"
echo "  │    └─┘└─┘┴└─ └┘ ┴└─┘└─┘  ┴└─┘  └─┘ ┴ ┴ ┴┴└─ ┴ ┴┘└┘└─┘  o o o   │                 │"
echo "  └────────────────────────────────────────────────────────────────┴─────────────────┘"

# for docker as environment
if [ "$ENVIRONMENT" = 'docker' ]; then
  $DOCKER_START
fi
