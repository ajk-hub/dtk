# Development Tool Kit

## How to install
- Create or copy `.user-preference.json` from [samples](https://github.com/ajk-hub/dtk/blob/main/samples/.user-preference.json)
in your home directory e.g. /home/dtk 
- Download dtk.zip file from [Release](https://github.com/ajk-hub/dtk/releases)
- Extract it and open terminal from there
```shell
chmod +x dtk
mv dtk /usr/local/bin
mv _dtk.zsh ~/.oh-my-zsh/completions/_dtk.zsh
```
- To confirm installation, type `dtk` in terminal 
- For completions type `dtk` and press tab


## For Development Use
- Create a virtual env for python : `python -m venv venv` 
- Install npm dependencies : `npm install`
- Enable husky : `npx husky install`

## Some Useful Commands
- dtk help
```
dtk
dtk -h
```

- dtk docker
```
dtk docker
dtk docker images
dtk docker images -s harbor
dtk docker build
dtk docker login
dtk docker login -i
dtk docker push
dtk docker push -t ashimjk/fixed-deposits-and-loans:248f14a0
dtk docker push -p
dtk docker bpush
```

- dtk maven
```
dtk maven
dtk maven clean
dtk maven install
dtk maven install -s
dtk maven install -s -m fixed-deposit
dtk maven deploy
dtk maven sonar
```

- dtk helm
```
dtk helm
dtk helm list
dtk helm status
dtk helm status beneficiary-backend
dtk helm status -d -s beneficiary-backend
dtk helm deploy -f beneficiary-dep.yaml beneficiary-backend
dtk helm deploy -f beneficiary-dep.yaml -s dtk beneficiary-backend
dtk helm deploy -v beneficiary,corpay-ui-shell:v1.72.23 dtk-test
dtk helm delete beneficiary-backend
dtk helm delete dtk-test
```

- dtk k6
```
dtk k6 run -v ./cicd/k6/api
dtk k6 run -v ./cicd/k6/api/000-fixed-deposit-request-create.js
```