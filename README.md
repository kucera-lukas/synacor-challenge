# synacor-challenge

My solution to the [Synacor Challange](https://challenge.synacor.com/) based on the [archived specification](https://github.com/Aneurysm9/vm_challenge)

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/kucera-lukas/synacor-challenge/main.svg)](https://results.pre-commit.ci/latest/github/kucera-lukas/synacor-challenge/main)

## Usage

### VM

```shell
python -m synacor spec/challenge.bin
```

### Adventure

```shell
python -m synacor adventure
```

### Dissassemble

```shell
python -m synacor disassemble spec/challenge.bin
```

### Coins

```shell
python -m synacor coins
```

### Energy level

```shell
rustc synacor/energy_level.rs
./energy_level
```

## Contributing

```shell
pre-commit install
```

## Credits

Based on the [archived specification](https://github.com/Aneurysm9/vm_challenge)

## License

Developed under the [MIT](https://github.com/kucera-lukas/synacor-challenge/blob/master/LICENSE) license.
