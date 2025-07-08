import yaml

file_path = r"C:\Users\Dhruba\Desktop\New folder\openapi.yaml"
with open(file_path, "r") as file:
    spec = yaml.safe_load(file)

base_url = spec["servers"][0]["url"]

generated_code = "import requests\n\n"

for path, methods in spec["paths"].items():
    for method, details in methods.items():
        func_name = details['summary'].lower().replace(" ", "_").replace("-", "_")
        parameters = details.get("parameters", [])
        func_args = []
        url_expr = f'f"{base_url + path}"'
        
        # build argument list
        for param in parameters:
            if param["in"] == "path":
                func_args.append(param["name"])
        
        args_str = ", ".join(func_args)
        
        # replace URL path with format expressions
        for param in parameters:
            if param["in"] == "path":
                url_expr = url_expr.replace(f"{{{param['name']}}}", f'{{{param["name"]}}}')

        generated_code += f"def {func_name}({args_str}):\n"
        generated_code += f"    url = {url_expr}\n"
        generated_code += f"    response = requests.{method.lower()}(url)\n"
        generated_code += f"    return response.json()\n\n"

# write to a file
with open("generated_api.py", "w") as f:
    f.write(generated_code)

print("✅ API client generated as 'generated_api.py'")