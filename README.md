## 1. Common Environment

- WSL(buntu 20.04.6 LTS)

## 2. READMEs

- [Ruby](./ruby/README.md)
- [Python](./python/README.md)

## 3. How to Use

In you terminal, provide the following 3 parameters via interactive user inputs.

- `username`: The default value is my username `hayat01sh1da`
- `unit`: Determine what unit your working report should be create in. The default value is `d`
  - Daily: `d`
  - Weekly: `w`
  - Monthly: `m`
- `year`: Determine what year's working report template you would like. The default value is the current year.
  - Creates templates only for weekday
  - Skips creating templates for leap days of every 4 years

### 3-1. For Ruby Lovers

```command
$ cd ./ruby/
$ ruby main.rb 
Provide your username(Default: hayat01sh1da)
hayat01sh1da
Provide your preferred unit d(daily - default), w(weekly) or m
d
Provide the specific year you would like to create working report templates for(Default: the current year)
2024
```

### 3-2. For Python Lovers

```command
$ cd ./python/
$ python main.py 
Provide your username(Default: hayat01sh1da): hayat01sh1da
Provide your preferred unit d(daily - default), w(weekly) or m: d
Provide the specific year you would like to create working report templates for(Default: the current year): 2024
```
