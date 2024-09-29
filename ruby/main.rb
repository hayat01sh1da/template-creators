require_relative './src/application'

puts 'Provide your username(Default: hayat01sh1da)'
_username = gets.chomp

puts 'Provide your preferred unit d(daily - default), w(weekly) or m(monthly)'
_unit = gets.chomp

puts 'Provide the specific year you would like to create working report templates for(Default: the current year)'
_year = gets.chomp

username = _username.empty? ? nil : _username
unit     = _unit.empty? ? nil : _unit
year     = _year.empty? ? nil : _year

if username && unit && year
  Application.run(username:, unit:, year:)
elsif username
  Application.run(username:)
elsif unit
  Application.run(unit:)
elsif year
  Application.run(year:)
else
  Application.run
end
