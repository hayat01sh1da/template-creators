require_relative './src/application'

unit, year, *_ = ARGV

if unit && year
  ::TemplateCreator::Application.run(unit:, year:)
elsif unit
  ::TemplateCreator::Application.run(unit:)
elsif year
  ::TemplateCreator::Application.run(year:)
else
  ::TemplateCreator::Application.run
end
