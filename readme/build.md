# Run All tests
    #Terminal settings:  Ensure terminal shell is configured to Gitbash
``` shell
    pushd ..
    export PATH=/c/Users/nites/anaconda3/condabin
    conda.bat env  update --name hackerrankquestions --file packaging/recipe.yml
    export PYTHONPATH=./src:./tests
    conda activate hackerrankquestions
    pytest tests/unit tests/integration 
```

```
Insall packages via :
conda.bat install -p C:/Users/nites/anaconda3/envs/hackerrankquestions lxml -y

```

```shell
  export PATH=/c/Users/nites/anaconda3/condabin
  conda --version



```