for service in "states" "lambda"; do
  service_dir=aws_openapi_dir/$service
  most_recent_schema_date=$(ls -1 $service_dir | tail -n 1)
  input_dir=$service_dir/$most_recent_schema_date
  input_schema=$(ls $input_dir/*.yaml | head -n 1)
  output_file=aws_interfaces/$service.py
  datamodel-codegen --input $input_schema --output $output_file --target-python-version 3.9 --enum-field-as-literal one --strict-nullable --collapse-root-models
done