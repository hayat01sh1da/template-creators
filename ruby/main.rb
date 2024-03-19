require_relative './src/application'

unit, year, *_ = ARGV

if unit && year
  ::TemplateCreator::Application.run(unit: unit, year: year)
elsif unit
  ::TemplateCreator::Application.run(unit: unit)
elsif year
  ::TemplateCreator::Application.run(year: year)
else
  ::TemplateCreator::Application.run
end
