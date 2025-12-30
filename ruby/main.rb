require_relative './src/application'

puts 'Provide your username(Default: hayat01sh1da)'
username = gets.chomp.strip

puts 'Provide your preferred unit d(daily - default), w(weekly) or m(monthly)'
unit = gets.chomp.strip

puts 'Provide the specific year you would like to create working report templates for(Default: the current year)'
year = gets.chomp.strip

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
