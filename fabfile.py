import sys
import time
from fabric import task
from fabric import Connection
from invoke import run as local
import csv
import requests
import sys
c = Connection('127.0.0.1')

@task
def deleteKindCluster(a):
     local('kind delete cluster')

@task
def createCluster(a):
     local('kind create cluster --config=./cluster.yml')

@task
def deployApp(c):
    local('./kubectl apply -f https://kind.sigs.k8s.io/examples/ingress/usage.yaml')

@task
def installHelm(c):
    local('curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3')
    local('chmod 700 get_helm.sh')
    local('./get_helm.sh')

@task
def deployNginxIngress(c):
    local('helm upgrade --install ingress-nginx ingress-nginx \
  --repo https://kubernetes.github.io/ingress-nginx \
  --namespace ingress-nginx --create-namespace --set controller.metrics.enabled=true \
--set-string controller.podAnnotations."prometheus\.io/scrape"="true" \
--set-string controller.podAnnotations."prometheus\.io/port"="10254" \
-f /Users/senthil.ar/Documents/hypen/nginx_ingress_values.yaml')
    local('./kubectl wait --namespace ingress-nginx --for=condition=ready pod --selector=app.kubernetes.io/component=controller --timeout=90s')

@task
def deployPrometheus(c):
    local('/Users/senthil.ar/Documents/hypen/kubectl apply --kustomize github.com/kubernetes/ingress-nginx/deploy/prometheus/')
    local('./kubectl apply -f ./prometheus_ingress.yaml')


@task
def loadTest(c,uri):
    li=list(uri.split(','))
    for i in li:
      local("ab -n 100 -c 10 http://localhost/"+i)

@task
def promtocsv(c, promUrl, filename, quries):
   print(quries)
   print(promUrl)
   with open(filename, 'w') as csvfile:
      response = requests.get('{0}/api/v1/query'.format(promUrl),
          params={'query': quries})
      results = response.json()['data']['result']

    # Build a list of all labelnames used.
      labelnames = set()
      for result in results:
        labelnames.update(result['metric'].keys())

    # lables
      labelnames.discard('__name__')
      labelnames = sorted(labelnames)

      writer = csv.writer(csvfile)
    # heading ROW
      writer.writerow(['name', 'timestamp', 'value'] + labelnames)

    # DATA ROW.
      for result in results:
        l = [result['metric'].get('__name__', '')] + result['value']
        for label in labelnames:
          l.append(result['metric'].get(label, ''))
        writer.writerow(l)
        


@task
def assessment(c, uriList='', promUrl='', filename='', quries=''):
  print("###################  Creating kind cluster ############################")
  time.sleep(2)
  createCluster(c)
  print("###################  Deploying the foo/bar ########################### ")
  time.sleep(2)
  deployApp(c)
  print("###################  Installing helm binary  ##########################")
  time.sleep(2)
  installHelm(c)
  print("##################  Deploying Nginx ingress  ##########################")
  time.sleep(2)
  deployNginxIngress(c)
  print("#################  Deploying Prometheus  ##############################")
  time.sleep(2)
  deployPrometheus(c)
  print("#################  Performing load test ###############################")
  time.sleep(2)
  loadTest(c,uriList)
  print("#################  CSV generation #####################################")
  time.sleep(2)
  promtocsv(c, promUrl, filename, quries)
