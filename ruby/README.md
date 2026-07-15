## 1. Environment

- Ruby 4.0.6
- Gemfile 4.0.14
- Bundler 4.0.14

## 2. Install Gems via Gemfile and Bundler

```command
$ bundle install
$ bundle lock --add-checksums
```

## 3. Execution

```command
$ rake run_template_creator
Provide your username(Default: hayat01sh1da)
hayat01sh1da
Provide your preferred unit d(daily - default), w(weekly) or m(monthly)
d
Provide the specific year you would like to create working report templates for(Default: the current year)
2024
```

## 4. Unit Test

```command
$ rake
Run options: --seed 39473

# Running:

........

Finished in 11.855362s, 0.6748 runs/s, 1.0966 assertions/s.

8 runs, 13 assertions, 0 failures, 0 errors, 0 skips
```

## 5. Static Code Analysis

```command
$ rubocop
Inspecting 5 files
.....

5 files inspected, no offenses detected
```

## 6. Type Checks

```command
$ rbs-inline --output sig/generated/ .
🎉 Generated 2 RBS files under sig/generated
$ steep check
# Type checking files:

....

No type error detected. 🫖
```
