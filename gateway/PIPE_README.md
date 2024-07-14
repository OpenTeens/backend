# gateway/pipe

## config
config file: `gateway/pipe_config.yaml`
```yaml
pipes:
  - name: <pipe name>   # the first one to execute
    rules:
      - path: "*"       # path match, using RegExp
        methods: "*"    # methods match, "*" / a list of methods
    processor:
      service: <service name>
      handler: <handler function name>
```
