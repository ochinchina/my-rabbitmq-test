# Install packages

install the following packages to all the node in the cluster

- erlang-18.3.4.6-1.el7.centos.x86_64.rpm
- rabbitmq-server-3.6.14-1.el7.noarch.rpm in the centos7

on each node, install the above package with following commands:

```shell
# rpm -ivh erlang-18.3.4.6-1.el7.centos.x86_64.rpm
# rpm -ivh rabbitmq-server-3.6.14-1.el7.noarch.rpm
```

# Create cluster

assume there are three nodes:

- node1
- node2
- node3


and in the node1, node2, node3, modify the /etc/hosts file to include the IP address of each node.

## Start the rabbitmq on node1

The rabbitmq can be started with systemctl:

```shell
# systemctl start rabbitmq-serveer
```

## Copy the /var/lib/rabbitmq/.erlang.cookie from node1 to node2 and node3

In node2 and node3, copy the file /var/lib/rabbitmq/.erlang.cookie from node1 with scp command:

```shell
# scp username@node1:/var/lib/rabbitmq/.erlang.cookie /var/lib/rabbitmq
```

## Join to the cluster

In node2 and node3, execute following command to jion to the cluster:

```shell
# systemctl start rabbitmq-server
# systemctl stop_app
# systemctl join_cluster rabbit@node1
Clustering node rabbit@node2 with rabbit@node1
```

## Check the rabbitmq cluster status

After a rabbitmq cluster is created, we need to check its status:

```shell
# systemctl cluster_status
Cluster status of node rabbit@node2
[{nodes,[{disc,[rabbit@node1,rabbit@node2,rabbit@node3]}]},
 {running_nodes,[rabbit@node1,rabbit@node2,rabbit@node3]},
 {cluster_name,<<"rabbit@node1">>},
 {partitions,[]},
 {alarms,[{rabbit@node1,[]},{rabbit@node2,[]}]},{rabbit@node3,[]}]}]

```
