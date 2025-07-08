import yaml
import requests
file_path = r"C:\Users\Dhruba\Desktop\New folder\openapi.yaml"
with open(file_path, "r") as file:
    spec = yaml.safe_load(file)

# Print the top level keys
print("Top level keys:", spec.keys())

# Print the servers
print("\nServers:")
for server in spec.get("servers", []):
    print(" -", server["url"])

# Print all paths
print("\nPaths and methods:")
for path, methods in spec["paths"].items():
    for method, details in methods.items():
        print(f" - {method.upper()} {path}: {details['summary']}")
#Detecting Parameters

print("\nDetecting Parameters")
for path , methods in spec["paths"].items():
    for method, details in methods.items():
        parameters=details.get("parameters",[])
        if parameters:
            print(f"\n{method.upper()}{path}")
        for param in parameters:
            name=param["name"]
            required=param.get("required",False)
            print(f" - Param : {name},required:{required}")

#Build Full urls with dummies

print("\nBuilding full URLs with dummy values:")
base_url = spec["servers"][0]["url"]

for path, methods in spec["paths"].items():
    for method, details in methods.items():
        url_path = path
        parameters = details.get("parameters", [])
        for param in parameters:
            if param["in"] == "path":
                url_path = url_path.replace(f"{{{param['name']}}}", "5")
        full_url = base_url + url_path
        print(f"{method.upper()} {full_url}")

#Calling Urls

print("\nCalling Urls with requests:")
for path, methods in spec["paths"].items():
    for method, details in methods.items():
        url_path = path
        parameters = details.get("parameters", [])
        for param in parameters:
            if param["in"] == "path":
                url_path = url_path.replace(f"{{{param['name']}}}", "5")
        full_url = base_url + url_path

        print(f"\n{method.upper()} {full_url}")
        
        if method.lower() == "get":
            response = requests.get(full_url)
            print("Status code:", response.status_code)
            try:
                print("Response JSON:", response.json())
            except:
                print("No JSON response.")
print("\nGenerating reusable Python functions:")

for path, methods in spec["paths"].items():
    for method, details in methods.items():
        func_name = details['summary'].lower().replace(" ", "_")
        parameters = details.get("parameters", [])
        func_args = []
        url_path = path
        for param in parameters:
            if param["in"] == "path":
                func_args.append(param["name"])
        
        # Build function signature
        args_str = ", ".join(func_args)
        if args_str:
            args_str = f"{args_str}"
        
        # Replace path parameters in URL
        url_expr = f'f"{base_url + path}"'
        for param in parameters:
            if param["in"] == "path":
                url_expr = url_expr.replace(
                    f"{{{param['name']}}}", f'{{{param["name"]}}}'
                )

        print(f"\ndef {func_name}({args_str}):")
        print(f"    url = {url_expr}")
        print(f"    response = requests.{method.lower()}(url)")
        print(f"    return response.json()")