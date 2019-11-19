# get-youtube-community

## require

* Docker
* pip
* Lambda Layer (Headless Chrome + chromedriver)

## install

./build_run.sh

upload `deploy_package.zip` to Lambda.

## execute in local

```
cp template.yaml.sample template.yaml
code template.yaml
```

edit template.yaml


```
sam invoke local --event mico.json
```
