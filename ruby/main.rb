require_relative './src/application'

puts 'Provide your username(Default: hayat01sh1da)'
username = gets.chomp.strip

puts 'Provide your preferred unit d(daily - default), w(weekly) or m(monthly)'
unit = gets.chomp.strip

puts 'Provide the specific year you would like to create working report templates for(Default: the current year)'
year = gets.chomp.strip

params = { username:, unit:, year: }.reject { |_, value| value.empty? }

Application.run(**params)
