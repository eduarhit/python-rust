# python-rust

This is a simple example of how to use Rust code in Python using pyo3.

No need to install rust or python to run this example, just need to have docker installed and run the following command:

```bash
jenkins@jenkins:~/python-rust$ docker compose run --rm dev
```
note: If you don't have docker installed, you can see [here](https://docs.docker.com/engine/install/debian/) ow to install it.

After running docker compose command above, you will be inside the container, you can then build the rust code and adapt it to python using maturin.
For example to use the rust code in the calculations_rs folder:
```bash 
jenkins@635baa5dfd7d:~/test-framework$ cd rust_projects/calculations_rs
jenkins@635baa5dfd7d:~/test-framework/rust_projects/calculations_rs$ maturin develop
```

Then you can go back to the root folder:
```bash
jenkins@635baa5dfd7d:~/test-framework/rust_projects/calculations_rs$ cd ../..
jenkins@635baa5dfd7d:~/test-framework$
```


And run the python code that uses the calculations_rs library:

```bash
jenkins@635baa5dfd7d:~/test-framework$ python3 measurements.py
```

note: the code is mounted in the container as a volume, so you can change the code in your local machine and run it in the container.

This is possible because these lines are in docker-compose file:

```yaml
    volumes:
      - ./:/home/$USER/test-framework
```



