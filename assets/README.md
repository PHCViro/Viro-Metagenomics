
```s

multiqc -f -v . --config ../../assets/multiqc_config.yml

# OR
docker run --rm -it -e USER=$USER -v $PWD:/data:rw  quay.io/biocontainers/multiqc:1.12--pyhdfd78af_0 

```

https://multiqc.info/docs/reports/customisation/#conditional-formatting