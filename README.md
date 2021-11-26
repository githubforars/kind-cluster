# kind-cluster
## Pre requests
`python3`
`fabric`

#### Disclaimer: The script is tested for MAC system. kubectl binary may not work for linux.


```
pip install fabric==2.5.0  csv requests
```

we can list all the fab commands using `fab -l`

```
$fab -l
Available tasks:

  assessment
  createCluster
  deleteKindCluster
  deployApp
  deployNginxIngress
  deployPrometheus
  installHelmKubectl
  loadTest
  promtocsv
```
## To get help
```
$fab --help assessment
Usage: fab [--core-opts] assessment [--options] [other tasks here ...]

Docstring:
  none

Options:
  -f STRING, --filename=STRING
  -p STRING, --promUrl=STRING
  -q STRING, --quries=STRING
  -u STRING, --uriList=STRING
```

###Sample run:
```
fab promtocsv 'http://localhost' 'cpu.csv' 'rate(nginx_ingress_controller_nginx_process_requests_total[2m])'
```


### To run complete once
```
fab assessment  --uriList='foo,bar' --promUrl='http://localhost' --filename='cpu.csv' --quries='sum(rate(nginx_ingress_controller_nginx_process_cpu_seconds_total[5m]))'

where
--uriList -> the service endpoint of deployed apps to perticipate on load test.
--promUrl -> prometheus url.
--filename -> filename for output csv to be written
--quries -> support single query
```
To perform multiple
```
fab promtocsv 'http://localhost' 'request_per_sec.csv' 'rate(nginx_ingress_controller_nginx_process_requests_total[2m])'
fab promtocsv 'http://localhost' 'avg_cpu_usage.csv' 'sum(rate(nginx_ingress_controller_nginx_process_cpu_seconds_total[5m]))'
fab promtocsv 'http://localhost' 'avg_mem_usage.csv' 'avg(nginx_ingress_controller_nginx_process_resident_memory_bytes)'
```



